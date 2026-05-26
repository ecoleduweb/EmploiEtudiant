from flask import request, Blueprint
from logging import getLogger
from app.services.user_service import UserService
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required
from app.dtos.user_dto import (
    UserUpdateDTO
)

user_service = UserService()

logger = getLogger(__name__)
user_blueprint = Blueprint('user', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@user_blueprint.route('/<int:id>', methods=['PUT'])
@token_required
def updateUser(current_user, id):
    dto = UserUpdateDTO.model_validate(request.get_json())
    dto.id = id
    updated = user_service.update_name_and_email(current_user, dto)
    return updated.model_dump(), 200

@user_blueprint.route('/all', methods=['GET'])
@token_admin_required
def get_all(current_user):
    users = user_service.get_all()
    return [u.model_dump() for u in users], 200

@user_blueprint.route('/toggleAdmin/<int:id>', methods=['PUT'])
@token_admin_required
def toggle_admin(current_user, id):
    dto = user_service.toggle_admin(current_user, id)
    return dto.model_dump(), 200
    
@user_blueprint.route('/<int:id>', methods=['DELETE'])
@token_admin_required
def delete(current_user, id):
    user_service.delete(current_user, id)
    return '', 204   
 
@user_blueprint.route('/toggleActive/<int:id>', methods=['PUT'])
@token_admin_required
def toggle_active(current_user, id):
    user = user_service.toggle_active(current_user, id)
    return user.model_dump(), 200
    
@user_blueprint.route('/<int:id>', methods=['GET'])
@token_admin_required
def get_user(current_user, id):
    dto = user_service.find_by_id(id)
    return dto.model_dump(), 200