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
import requests
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

        jobOffer = jobOffer_service.createJobOffer(data["jobOffer"], employer.id, isApproved, current_user.id)
        for studyProgramId in data["studyPrograms"]:
            offer_program_service.linkOfferProgram(studyProgramId, jobOffer.id)
        
        employment_schedule_service.linkOfferSchedule(data["scheduleIds"], jobOffer.id)
        
        enterprise = enterprise_service.getEnterprise(employer.enterpriseId)
    
        sendMail(current_user.email, "Accusé de réception - Création d'une nouvelle offre d'emploi", "Votre offre d'emploi (<b>" + jobOffer.title + "</b>) a bien été créée. Celle-ci sera affichée publiquement lorsqu'elle sera approuvée. <br> Veuillez prévoir un délai moyen de 24 à 48 heures ouvrables. <br>Vous recevrez un courriel lorsque votre offre sera affichée sur le Portail d'offres d'emploi du Cégep de Rivière-du-Loup. <br><br>Merci d'avoir soumis votre offre!")
        sendMail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Création d'une nouvelle offre d'emploi", "Une nouvelle offre d'emploi a été créée du nom de <b>" + jobOffer.title + "</b> par <b>" + current_user.firstName + "</b> <b>" + current_user.lastName + "</b>, pour l'entreprise " + enterprise.name + ".")
        return jobOffer.to_json_string(), 201
    except Exception as e:
        print("10")
        logger.warning("Could not create jobOffer, invalid data : " + str(e))
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
        logger.warning(f'Job offer not found with id : {id}')
        return jsonify({'message': 'offre d\'emploi non trouvée'}), 404

@job_offer_blueprint.route('/employer/all', methods=['GET'])
@token_required
def offresEmploiEmployeur(current_user):
    needsEntrepriseDetails = request.args.get("entrepriseDetails") == "true"
    needsEmploymentScheduleDetails = request.args.get("employmentScheduleDetails") == "true"
    needsStudyProgramDetails = request.args.get("studyProgramDetails") == "true"
    if current_user.isModerator:
        jobOffers = jobOffer_service.offresEmploi(needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
        return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])
    #Si il n'y a pas d'offre d'emploi pour l'employeur, on retourne un tableau vide
    try:
        employerId = employer_service.getEmployerByUserId(current_user.id).id
    except Exception as e:
        logger.warning('Employer not found : ' + str(e))
        return jsonify([]), 404
    jobOffers = jobOffer_service.offresEmploiEmployeur(employerId, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
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
            jobOfferToUpdate.last_modified_by_id = current_user.id
        
        jobOffer = jobOffer_service.updateJobOffer(data)
        employment_schedule_service.linkOfferSchedule(data["scheduleIds"], jobOffer.id)
        # update offerProgram
        if 'studyPrograms' in data:
            offer_program_service.updateOfferProgram(jobOffer.id, data['studyPrograms'])
        if jobOffer:
            if not current_user.isModerator:
                sendMail(current_user.email, "Modification d'une offre d'emploi", "L'offre d'emploi au nom de <b>" + jobOffer.title + "</b> a été modifiée avec succès. <br> Veuillez prévoir un délai moyen de 24 à 48 heures ouvrables pour la mise à jour de votre offre. <br> Vous recevrez un courriel lorsque votre offre modifiée sera affichée sur le Portail d'offres d'emploi du Cégep de Rivière-du-Loup. ")
            else:
                sendMail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Confirmation de modification d'une offre d'emploi", "L'offre d'emploi au nom de <b>" + jobOffer.title + "</b> a été modifiée avec succès.")
            return jsonify(jobOffer.to_json_string()), 200
    logger.warning('Job offer not found with data : ' + str(data))
    return jsonify({'message': 'Job offer not found'}), 404

@job_offer_blueprint.route('/approved', methods=['GET'])
def offresEmploiApproved():
    getRecentOnly = request.args.get("getRecentOnly") == "true"
    getEntrepriseDetails = request.args.get("entrepriseDetails") == "true"
    employmentScheduleDetails = request.args.get("employmentScheduleDetails") == "true"
    studyProgramDetails = request.args.get("studyProgramDetails") == "true"

    if getRecentOnly:
        jobOffers = jobOffer_service.getRecentOffers(getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
        return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])
    else:
        jobOffers = jobOffer_service.getOffers(getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
        return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])

@job_offer_blueprint.route('/approve/<int:id>', methods=['PUT'])
@token_admin_required
def approveJobOffer(current_user, id):
    linking = request.args.get("linking") == "true"
    jobOfferToUpdate = jobOffer_service.findById(id)
    if jobOfferToUpdate:
        data = request.get_json()
        if linking:
            user_service.linkToExisting(jobOfferToUpdate, data['selectedEnterpriseId'])
        jobOffer_service.approveJobOffer(id, data['isApproved'], data['approbationMessage'])
        
        print(jobOfferToUpdate)
        current_user_job = User.query.filter_by(id=jobOfferToUpdate.last_modified_by_id ).first()
        print(current_user_job)

        if data['isApproved'] == True:
            sendMail(current_user_job.email, "Approbation d'une offre d'emploi", "L'offre d'emploi au nom de <b>" + jobOfferToUpdate.title + "</b> a été approuvée.")
        else:
            sendMail(current_user_job.email, "Approbation d'une offre d'emploi", "L'offre d'emploi au nom de <b>" + jobOfferToUpdate.title + "</b> a été refusée.<br>Raison: " + jobOfferToUpdate.approbationMessage)
        return ('', 204)
    logger.warning('Job offer not found with data : ' + str(data))
    return jsonify({'message': 'Job offer not found'}), 404

@job_offer_blueprint.route('/archive/<int:id>', methods=['POST'])
@token_required
def archiveJobOffer(current_user, id):
    try:
        jobOffer_service.archiveJobOffer(id)
        return ('', 204)
    except NotFoundException as e:
        logger.warning('Study Program not found with id : ' + str(id))
        return jsonify({'message': e.message}), e.errorCode
    
@job_offer_blueprint.route('/verifyURL', methods=['POST'])
def verify_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(url)
        if response.ok:
            return jsonify({'message': 'URL is accessible'}), 200
        else:
            return jsonify({'error': 'URL is not accessible'}), 404
    except requests.RequestException as e:
        return jsonify({'error': 'URL is not accessible', 'details': str(e)}), 404
