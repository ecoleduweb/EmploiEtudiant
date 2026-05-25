from flask import jsonify, request, Blueprint
from flask import Flask, jsonify, request, make_response
from app.services.enterprise_service import EnterpriseService
from app.services.user_service import UserService
from app.middleware.adminTokenVerified import token_admin_required
from app.middleware.tokenVerify import token_required
from app.dtos.enterprise_dto import (
    EnterpriseCreateDTO,
    EnterpriseUpdateDTO
)

from logging import getLogger
enterprise_service = EnterpriseService()

logger = getLogger(__name__)
enterprise_blueprint = Blueprint('enterprise', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@enterprise_blueprint.route('/all', methods=['GET'])
@token_admin_required
def get_all(current_user):
    enterprises = enterprise_service.get_all()
    return [sp.model_dump() for sp in enterprises], 200

@enterprise_blueprint.route('/new', methods=['POST'])
@token_admin_required
def create_enterprise(current_user):
    dto = EnterpriseCreateDTO.model_validate(request.get_json())
    created = enterprise_service.create(dto, False)
    return created.model_dump(), 201

@enterprise_blueprint.route('/<int:id>', methods=['PUT'])
@token_required
def update_enterprise(current_user, id):
    dto = EnterpriseUpdateDTO.model_validate(request.get_json())
    dto.id = id
    updated = enterprise_service.update(dto, current_user)
    return updated.model_dump(), 200


@enterprise_blueprint.route('/<int:id>', methods=['GET'])
@token_required
def get_enterprise(current_user, id):
    dto = enterprise_service.find_by_id(id)
    return dto.model_dump(), 200
    
@enterprise_blueprint.route('/currentEnterprise', methods=['GET'])
@token_required
def getCurrentUserEnterprise(current_user):
    dto = enterprise_service.find_by_id(current_user.enterpriseId)
    return dto.model_dump(), 200
