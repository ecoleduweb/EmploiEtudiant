from flask import jsonify,request, Blueprint
import os
from logging import getLogger
import json
from app.middleware.tokenVerify import token_required
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from datetime import datetime
from app.utils.Encryption import decrypt
from app.dtos.user_dto import (
    UserRegisterDTO,
    UserLoginDTO,
    UserUpdatePasswordDTO
)

auth_service = AuthService()
user_service = UserService()

from logging import getLogger

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
    try:
        data = request.get_json()
        decryptedData = json.loads(decrypt(data['token']))
        if data['password'] == data['confirmPassword']:
            try:
                reset_date = float(decryptedData['resetDate'])
                if (reset_date + 900) > datetime.now().timestamp():
                    user_service.update_reset_password(decryptedData['email'], data['password'])
                    return jsonify({'message': 'Successfully resetted the password'})
                else:
                    logger.warning("A user tried to reset the password via a expired link")
                    return jsonify({'message': 'Error while trying to reset the password (Link expired)'}), 403
            except Exception as e:
                logger.warning("A user tried to reset the password but it failed")
                return jsonify({'message': 'Error while trying to reset the password'}), 401
    except Exception as e:
        return jsonify({'message': 'Error while trying to reset the password, is token valid?'}), 403


def _generate_auth_response(user, token):
    response = jsonify({
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