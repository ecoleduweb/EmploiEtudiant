from flask import request, Blueprint
from app.services.study_program_service import StudyProgramService
from app.middleware.adminTokenVerified import token_admin_required
from app.middleware.tokenVerify import token_required

from logging import getLogger
from app.dtos.study_program_dto import (
    StudyProgramCreateDTO,
    StudyProgramUpdateDTO
)

logger = getLogger(__name__)
study_program_service = StudyProgramService()

study_program_blueprint = Blueprint('studyProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/


@study_program_blueprint.route('/studyPrograms', methods=['GET'])
def get_all():
    studyPrograms = study_program_service.find_all()
    return [sp.model_dump() for sp in studyPrograms], 200

@study_program_blueprint.route('/studyProgram/<int:id>', methods=['PUT'])
@token_admin_required
def update(current_user, id):
    dto = StudyProgramUpdateDTO.model_validate(request.get_json())
    dto.id = id
    updated = study_program_service.update(dto)
    return updated.model_dump(), 200
    

    
@study_program_blueprint.route('/new', methods=['POST'])
@token_admin_required
def create(current_user):
    dto = StudyProgramCreateDTO.model_validate(request.get_json())
    created = study_program_service.create(dto)
    return created.model_dump(), 201