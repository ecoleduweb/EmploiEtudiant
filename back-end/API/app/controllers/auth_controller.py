from flask import jsonify,request, Blueprint
import os
from logging import getLogger
import json
from app.middleware.tokenVerify import token_required
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.utils.Encryption import decrypt
from app.dtos.user_dto import (
    UserRegisterDTO,
    UserLoginDTO,
    UserUpdatePasswordDTO
)

auth_service = AuthService()
user_service = UserService()


logger = getLogger(__name__)
auth_blueprint = Blueprint('auth', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@auth_blueprint.route('/login', methods=['POST'])
def login():
    dto = UserLoginDTO.model_validate(request.get_json())
    token, user = auth_service.login(dto)
    return _generate_auth_response(user, token)

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
        resp =jsonify({"message":'Logged out successfully'}) 
        resp.delete_cookie("token", path="/")
        return resp
    
@auth_blueprint.route('/register', methods=['POST'])
def register():
    dto = UserRegisterDTO.model_validate(request.get_json())
    token, user = auth_service.register(dto)
    return _generate_auth_response(user, token)

@auth_blueprint.route("/me", methods=['GET'])
@token_required
def me(current_user):
    return user_service.find_by_id(current_user.id).model_dump(), 200

@auth_blueprint.route('/updatePassword/<int:id>', methods=['PUT'])
@token_required
def updatePassword(current_user, id):
    dto = UserUpdatePasswordDTO.model_validate(request.get_json())
    dto.id = id
    user = user_service.update_password(current_user, dto)
    return user.model_dump(), 200

@auth_blueprint.route('/resetPassword', methods=['POST'])
def resetPassword():
    data = request.get_json()
    auth_service.request_reset_password(data['email'])
    return {'message': 'Mise à jour réussie'}, 200

@auth_blueprint.route('/requestResetPassword', methods=['POST'])
def requestResetPassword():
    data = request.get_json()
    decryptedData = json.loads(decrypt(data['token']))
    auth_service.reset_password(decryptedData['email'], data['password'], float(decryptedData['resetDate']))
    return {'message': 'Envoie du courriel réussi'}, 200

def _generate_auth_response(user, token):
    response = jsonify({
        'id': user.id,
        "isModerator": user.isModerator,
        "email": user.email,
        "firstName": user.firstName,
        "lastName": user.lastName
    })

    secure_cookie = os.environ.get("COOKIE_SECURE", "True") != "False"
    response.set_cookie(
        'token', 
        token, 
        httponly=True, 
        samesite='Lax', 
        secure=secure_cookie, 
        max_age=60 * 30, 
        path='/'
    )
    
    return response, 200