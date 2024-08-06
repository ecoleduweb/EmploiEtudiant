from flask import jsonify, request, Blueprint, current_app
from datetime import datetime
import os
from app.models.user_model import User
from app.models.employers_model import Employers
from jwt import decode
from app.services.jobOffer_service import JobOfferService
from app.services.employer_service import EmployerService
from app.services.enterprise_service import EnterpriseService
from app.services.user_service import UserService
from app.services.offer_program_service import OfferProgramService
from app.services.study_program_service import StudyProgramService
from app.services.employmentSchedule_service import EmploymentScheduleService
jobOffer_service = JobOfferService()
employer_service = EmployerService()
enterprise_service = EnterpriseService()
user_service = UserService()
offer_program_service = OfferProgramService()
study_program_service = StudyProgramService()
employment_schedule_service = EmploymentScheduleService()
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required
from logging import getLogger
from app.services.email_service import sendMail
from app.customexception.CustomException import NotFoundException
import os

logger = getLogger(__name__)
job_offer_blueprint = Blueprint('jobOffer', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@job_offer_blueprint.route('/new', methods=['POST'])
@token_required
def createJobOffer(current_user):
    try:
        data = request.get_json()
        if current_user.isModerator:
            isApproved = True

            if data["enterprise"]["id"] != None and data["enterprise"]["id"] != 0:
                employer = employer_service.createEmployer(data["enterprise"]["id"], None)
            else:
                return jsonify({'message', 'No enterprise selected.'}), 400
        else:
            # None implque qu'il n'est ni à False ni à True donc en attent d'approbation.
            isApproved = None
            employer = Employers.query.filter_by(userId=current_user.id).first()
            # Quand un employeur crée pour la première fois une offre, on crée aussi son entreprise.
            if employer is None:
                enterprise = enterprise_service.createEnterprise(data["enterprise"], True)
                enterpriseId = enterprise_service.getEnterpriseId(enterprise.name)
                employer = employer_service.createEmployer(enterpriseId, current_user.id)

        jobOffer = jobOffer_service.createJobOffer(data["jobOffer"], employer.id, isApproved)
        for studyProgramId in data["studyPrograms"]:
            offer_program_service.linkOfferProgram(studyProgramId, jobOffer.id)
        
        employment_schedule_service.linkOfferSchedule(data["scheduleIds"], jobOffer.id)
        
        
        sendMail(current_user.email, "Accusé de réception - Création d'une nouvelle offre d'emploi", "Votre offre d'emploi (" + jobOffer.title + ") à bien été créée. \nVotre offre sera public lorsqu'il sera vérifier.")
        sendMail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Création d'une nouvelle offre d'emploi", "Une nouvelle offre d'emploi a été créée du nom de " + jobOffer.title + ".")

        return jobOffer.to_json_string(), 201
    except Exception as e:
        logger.warn("Could not create jobOffer, invalid data")
        return jsonify({'message': 'Could not create jobOffer, invalid data'}), 400

@job_offer_blueprint.route('/<int:id>', methods=['GET'])
def offreEmploi(id):
    needsEntrepriseDetails = request.args.get("entrepriseDetails") == "true"
    needsEmploymentScheduleDetails = request.args.get("employmentScheduleDetails") == "true"
    needsStudyProgramDetails = request.args.get("studyProgramDetails") == "true"

    jobOffer = jobOffer_service.findById(id)
    if jobOffer:
        jobOfferDetails = jobOffer_service.getInfo(jobOffer, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
        return jsonify(jobOfferDetails.to_json_string())
    else:
        logger.warn(f'Job offer not found with id : {id}')
        return jsonify({'message': 'offre d\'emploi non trouvée'}), 404

@job_offer_blueprint.route('/employer/all', methods=['GET'])
@token_required
def offresEmploiEmployeur(current_user):
    if current_user.isModerator:
        jobOffers = jobOffer_service.offresEmploi()
        return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])
    #Si il n'y a pas d'offre d'emploi pour l'employeur, on retourne un tableau vide
    try:
        employerId = employer_service.getEmployerByUserId(current_user.id).id
    except Exception as e:
        logger.warn('Employer not found : ' + str(e))
        return jsonify([]), 404
    jobOffers = jobOffer_service.offresEmploiEmployeur(employerId)
    return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])

@job_offer_blueprint.route('/<int:id>', methods=['PUT'])
@token_required
def updateJobOffer(current_user, id):
    jobOfferToUpdate = jobOffer_service.findById(id)
    if jobOfferToUpdate:
        data = request.get_json()
        # ACM Mettre toute la logique dans le service.
        if not current_user.isModerator:
            data["jobOffer"]["isApproved"] = None
            data["jobOffer"]["approbationMessage"] = None
            # ACM Ajouter une logique pour envoyer un message à l'admin d'approver l'offre si l'offre change de statut.
            # Une offre qui a le même contenu (le message d'explication de l'offre) devrait restée approuvée.
            if data["jobOffer"]["isApproved"] == True:
                data["jobOffer"]["approvedDate"] = datetime.now()

        jobOffer = jobOffer_service.updateJobOffer(data)
        employment_schedule_service.linkOfferSchedule(data["scheduleIds"], jobOffer.id)
        # update offerProgram
        if 'studyPrograms' in data:
            offer_program_service.updateOfferProgram(jobOffer.id, data['studyPrograms'])
        if jobOffer:
            sendMail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Modification d'une offre d'emploi", "L'offre d'emploi avec le nom " + jobOffer.title + " a été modifiée.")
            
            return jsonify(jobOffer.to_json_string()), 200
    logger.warn('Job offer not found with data : ' + str(data))
    return jsonify({'message': 'Job offer not found'}), 404

@job_offer_blueprint.route('/approved', methods=['GET'])
def offresEmploiApproved():
    getRecentOnly = request.args.get("getRecentOnly") == "true"

    if getRecentOnly:
        jobOffers = jobOffer_service.getRecentOffers()
        return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])
    else:
        jobOffers = jobOffer_service.getOffers()
        return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])

@job_offer_blueprint.route('/approve/<int:id>', methods=['PUT'])
@token_admin_required
def approveJobOffer(current_user, id):
    linking = request.args.get("linking") == "true"
    jobOfferToUpdate = jobOffer_service.findById(id)
    if jobOfferToUpdate:
        data = request.get_json()
        if linking:
            user_service.linkToExisting(id, data['isApproved'], data['approbationMessage'])
        user_service.linkToExisting(jobOfferToUpdate, data['selectedEnterpriseId'])
        jobOffer_service.approveJobOffer(id, data['isApproved'], data['approbationMessage'])
        # ACM un beau petit travail ici pour trouver le courriel du propriétaire du courriel et ensuite lui envoyer un courriel

        if data['isApproved'] == True:
            sendMail(current_user.email, "Approbation d'une offre d'emploi", "L'offre d'emploi avec le nom " + jobOfferToUpdate.title + " a été approuvée.")
        else:
            sendMail(current_user.email, "Approbation d'une offre d'emploi", "L'offre d'emploi avec le nom " + jobOfferToUpdate.title + " a été refusée.<br>Raison: " + jobOfferToUpdate.approbationMessage)
        return ('', 204)
    logger.warn('Job offer not found with data : ' + str(data))
    return jsonify({'message': 'Job offer not found'}), 404

@job_offer_blueprint.route('/archive/<int:id>', methods=['POST'])
@token_required
def archiveJobOffer(current_user, id):
    try:
        jobOffer_service.archiveJobOffer(id)
        return ('', 204)
    except NotFoundException as e:
        logger.warn('Study Program not found with id : ' + str(id))
        return jsonify({'message': e.message}), e.errorCode