from flask import jsonify, request, Blueprint, current_app
import os
from app.models.user_model import User
from app.services.jobOffer_service import JobOfferService
from app.services.enterprise_service import EnterpriseService
from app.services.user_service import UserService
from app.services.study_program_service import StudyProgramService
from app.services.employmentSchedule_service import EmploymentScheduleService
from app.dtos.job_offer_dto import (
    JobOfferCreateDTO,
    JobOfferUpdateDTO, 
    JobOfferApproveDTO
)
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required
from logging import getLogger
from app.services.email_service import send_mail
import requests
import os
from app.utils.SanitizeDOM import sanitize_html

job_offer_service = JobOfferService()
enterprise_service = EnterpriseService()
user_service = UserService()
study_program_service = StudyProgramService()
employment_schedule_service = EmploymentScheduleService()

logger = getLogger(__name__)
job_offer_blueprint = Blueprint('jobOffer', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@job_offer_blueprint.route('/new', methods=['POST'])
@token_required
def create_job_offer(current_user):
    dto = JobOfferCreateDTO.model_validate(request.get_json())
    job_offer = job_offer_service.create(current_user, dto)
    return job_offer.model_dump(), 201

@job_offer_blueprint.route('/<int:id>', methods=['GET'])
def get_job_offer(id):
    needsentreprise_details = request.args.get("entrepriseDetails") == "true"
    needsemployment_schedule_details = request.args.get("employmentScheduleDetails") == "true"
    needsstudy_program_details = request.args.get("studyProgramDetails") == "true"

    dto = job_offer_service.find_by_id(id, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details)
    return dto.model_dump(), 200

@job_offer_blueprint.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_job_offer(current_user, id):
    job_offer_service.delete_by_id(current_user,id)
    return '', 204


@job_offer_blueprint.route('/<int:id>', methods=['PUT'])
@token_required
def update_job_offer(current_user, id):
    dto = JobOfferUpdateDTO.model_validate(request.get_json())  
    dto.id = id
    jobOffer = job_offer_service.update(current_user, dto)
    return jobOffer.model_dump(), 200

@job_offer_blueprint.route('/employer/all', methods=['GET'])
@token_required
def enterprise_job_offers(current_user):
    needsentreprise_details = request.args.get("entrepriseDetails") == "true"
    needsemployment_schedule_details = request.args.get("employmentScheduleDetails") == "true"
    needsstudy_program_details = request.args.get("studyProgramDetails") == "true"
    if current_user.isModerator:
        jobOffers = job_offer_service.all(needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details)
    else: 
        jobOffers = job_offer_service.find_enterprises_job_offer_by_user_id(current_user.id, needsentreprise_details, needsemployment_schedule_details, needsstudy_program_details)
    return [jo.model_dump() for jo in jobOffers], 200


@job_offer_blueprint.route('/approved', methods=['GET'])
def get_approved_job_offers():
    get_entreprise_details = request.args.get("entrepriseDetails") == "true"
    employment_schedule_details = request.args.get("employmentScheduleDetails") == "true"
    study_program_details = request.args.get("studyProgramDetails") == "true"

    jobOffers = job_offer_service.get_all(get_entreprise_details, employment_schedule_details, study_program_details)
    return [jo.model_dump() for jo in jobOffers], 200

@job_offer_blueprint.route('/approve/<int:id>', methods=['PUT'])
@token_admin_required
def approve_job_offer(current_user, id):
    dto = JobOfferApproveDTO.model_validate(request.get_json())
    dto.id = id
    job_offer = job_offer_service.approve(dto)
    return job_offer.model_dump(), 200

@job_offer_blueprint.route('/archive/<int:id>', methods=['POST'])
@token_required
def archive_job_offer(current_user, id):
    dto =job_offer_service.archive(id)
    return dto.model_dump(), 200

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
