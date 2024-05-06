from flask import jsonify, request, Blueprint
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

job_offer_blueprint = Blueprint('jobOffer', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@job_offer_blueprint.route('/createJobOffer', methods=['POST'])
@token_required
def createJobOffer(current_user):
    data = request.get_json()
    token = request.headers.get('Authorization')
    decoded_token = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    user = User.query.filter_by(email = decoded_token['email']).first()
    employer = None
    if user.isModerator:
        employer = employer_service.createEmployer(data["enterprise"]["id"], None)
        isApproved = True
    else:
        isApproved = None
        employer = Employers.query.filter_by(userId=user.id).first()
        if employer is None:
            entreprise = enterprise_service.createEnterprise(data["enterprise"], True)
            entrepriseId = enterprise_service.getEntrepriseId(entreprise.name)
            employer = employer_service.createEmployer(entrepriseId, user.id)
    jobOffer = jobOffer_service.createJobOffer(data["jobOffer"], employer.id, isApproved)
    for studyProgram in data["studyPrograms"]:
        studyProgramId = study_program_service.studyProgramId(studyProgram)
        offerProgram = offer_program_service.linkOfferProgram(studyProgramId, jobOffer.id)
    return jsonify({'message': 'Job offer created successfully'})

@job_offer_blueprint.route('/offreEmploi', methods=['GET'])
def offreEmploi():
    id = request.args.get('id')
    jobOffer = jobOffer_service.offreEmploi(id)
    if jobOffer:
        return jsonify(jobOffer.to_json_string())
    else:
        return jsonify({'message': 'offre d\'emploi non trouvée'}), 404

@job_offer_blueprint.route('/offresEmploiEmployeur', methods=['GET'])
@token_required
def offresEmploiEmployeur(current_user):
    token = request.headers.get('Authorization')
    decoded_token = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    user = User.query.filter_by(email = decoded_token['email']).first()
    if user.isModerator:
        jobOffers = jobOffer_service.offresEmploi()
        return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])
    #Si il n'y a pas d'offre d'emploi pour l'employeur, on retourne un tableau vide
    try:
        employerId = employer_service.getEmployerByUserId(user.id).id
    except Exception as e:
        return jsonify([]), 200
    jobOffers = jobOffer_service.offresEmploiEmployeur(employerId)
    return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])

@job_offer_blueprint.route('/updateJobOffer', methods=['PUT'])
@token_required
def updateJobOffer(current_user):
    data = request.get_json()
    jobOffer = jobOffer_service.updateJobOffer(data)
    print(data['studyPrograms'])
    # update offerProgram
    if 'studyPrograms' in data:
        offer_program_service.updateOfferProgram(jobOffer.id, data['studyPrograms'])

    if jobOffer:
        return jsonify(jobOffer.to_json_string())
    else:
        return jsonify({'message': 'Job offer not found'}), 404

@job_offer_blueprint.route('/offresEmploi', methods=['GET'])
def offresEmploi():
    jobOffers = jobOffer_service.offresEmploi()
    return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])

@job_offer_blueprint.route('/offresEmploiApproved', methods=['GET'])
def offresEmploiApproved():
    jobOffers = jobOffer_service.offresEmploiApproved()
    return jsonify([jobOffer.to_json_string() for jobOffer in jobOffers])

@job_offer_blueprint.route('/linkJobOfferEmployer', methods=['PUT'])
@token_required
def linkJobOfferEmployer(current_user):
    data = request.get_json()
    return jobOffer_service.linkJobOfferEmployer(data)

@job_offer_blueprint.route('/approveJobOffer', methods=['PUT'])
@token_admin_required
def approveJobOffer(current_user):
    data = request.get_json()
    return jobOffer_service.approveJobOffer(data)
