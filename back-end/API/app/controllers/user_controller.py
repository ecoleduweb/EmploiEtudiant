from flask import jsonify, request, Blueprint
import os
from logging import getLogger
from jwt import decode
import json
from app.services.user_service import UserService
from app.services.employer_service import EmployerService
from app.services.enterprise_service import EnterpriseService
from app.services.jobOffer_service import JobOfferService
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required
from app.customexception.CustomException import LoginException
from app.services.email_service import sendMail
from datetime import datetime
from app.utils.Encryption import encrypt, decrypt
from app.repositories.auth_repo import AuthRepo

auth_repo = AuthRepo()

joboffer_service = JobOfferService()
user_service = UserService()
employer_service = EmployerService()
enterprise_service = EnterpriseService()
from logging import getLogger

logger = getLogger(__name__)
user_blueprint = Blueprint('user', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@user_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        token = user_service.login(data["email"], data["password"])
        return jsonify({'token' : token})
    except LoginException as e:
        if data["email"] != "" and data["email"] != None:
            if len(data["email"]) <= 255:
                logger.warn("User (" + data["email"] + ") failed to login. Error message: " + e.message)
            else:
                logger.warn("User (EMAIL TOO BIG TO DISPLAY) failed to login and provided a huge email. Error message: " + e.message)
            return jsonify({'message': e.message}), e.errorCode
        else:
            logger.warn("An unauthentificated user tried logging without an email.")
            return jsonify({'message': "Impossible de se connecter: aucun email à été fournis"}), 401
    
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all([data.get('email'), data.get('password'), data.get('firstName'), data.get('lastName'), data.get('captchaToken')]):
        logger.warn('Missing required fields in /register : ' + str(data))
        return jsonify({'message': 'Missing required fields'}), 400
    
    if not isinstance(data, dict):
        logger.warn('Invalid JSON data format in /register : ' + str(data))
        return jsonify({'message': 'Invalid JSON data format'}), 400

    if user_service.getUser(data['email']) == "<Response 29 bytes [200 OK]>" or user_service.getUser(data['email']) is not None:
        logger.warn('User already exists')
        return jsonify({'message': 'User already exists'}), 400

    return user_service.register(data)

@user_blueprint.route('/updatePassword', methods=['PUT'])
@token_required
def updatePassword(current_user):
    data = request.get_json()
    
    if not isinstance(data, dict):
        logger.warn('Invalid JSON data format in /updatePassword : ' + str(data))
        return jsonify({'message': 'Invalid JSON data format'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        logger.warn('Missing required fields in /updatePassword : \nEmail :' + email + ' \nPassword : ' + password)
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        user_service.updatePassword(current_user, data)
        return jsonify({'message': 'password updated'})
    except Exception as e:
        userEmail = ""

        if current_user.isModerator:
            userEmail = data["email"]
        else:
            userEmail = current_user.email

        logger.warn("Failed to update password for email: " + userEmail, e)
        return jsonify({'message': "could not change password"}), 500

@user_blueprint.route('/user', methods=['PUT'])
@token_required
def updateUser(current_user):
    data = request.get_json()

    if not isinstance(data, dict):
        logger.warn('Invalid JSON data format in /user : ' + str(data))
        return jsonify({'message': 'Invalid JSON data format'}), 400
    
    lastname = data.get('lastname')
    firstname = data.get('firstname')
    email = data.get('email')
    
    if not all([lastname, firstname, email]):
        logger.warn('Missing required fields in /user : \nname : ' + str(lastname) + ' \nfirstname: ' + str(firstname) + ' \nemail: ' + str(email))
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        user_service.updateUser(current_user, data)
        return jsonify({'message': 'user updated'})
    except Exception as e:
        userEmail = ""

        if current_user.isModerator:
            userEmail = data["email"]
        else:
            userEmail = current_user.email

        logger.warn("Failed to update user with email: " + userEmail, e)
        return jsonify({'message': 'could not update user'}), 500

@user_blueprint.route('/all', methods=['GET'])
@token_admin_required
def getAllUsers(current_user):
    response = user_service.getAllUsers()
    return response


@user_blueprint.route('/getUser', methods=['GET'])
@token_required
def getUser(current_user):
    token = request.headers.get('Authorization')
    data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    email = data['email']
    if not token:
        logger.warn('Token not provided to get user')
        return jsonify({'message': 'Token not provided'}), 400
    user = user_service.getUser(email)
    return jsonify(user.to_json_string())

@user_blueprint.route('/makeAdmin', methods=['PUT'])
@token_admin_required
def makeAdmin(current_user):
    try:
        data = request.get_json()
        user_service.makeAdmin( user_service.getUser(data['email']) )
        return jsonify({'message': 'Successfully updated user (' + data['email'] + ')'})
    except Exception as e:
        logger.error('Couldn\'t update user (' + data['email'] + ')')
        return jsonify({'message': 'Couldn\'t update user (' + data['email'] + ')'}), 500
    
@user_blueprint.route('/deleteUser', methods=['PUT'])
@token_admin_required
def deleteUser(current_user):
    try:
        data = request.get_json()
        user_service.removeUser(current_user, data['email'])
        return jsonify({'message': 'Successfully removed user (' + data['email'] + ')'})
    except Exception as e:
        logger.error('Couldn\'t remove user (' + data['email'] + ')')
        return jsonify({'message': 'Couldn\' remove user (' + data['email'] + ')'}), 500
    
@user_blueprint.route('/desactivateUser', methods=['PUT'])
@token_admin_required
def desactivateUser(current_user):
    try:
        data = request.get_json()
        user_service.desactivateUser(current_user, data['email'])
        return jsonify({'message': 'Successfully desactivated user (' + data['email'] + ')'})
    except Exception as e:
        logger.error('Couldn\'t desactivate user (' + data['email'] + ')')
        return jsonify({'message': 'Couldn\'t desactivate user (' + data['email'] + ')'}), 500
    
@user_blueprint.route('/requestResetPassword', methods=['POST'])
def requestResetPassword():
    try:
        data = request.get_json()

        if user_service.getUser(data['email']):
            userData = {
                "email": data['email'],
                "resetDate": datetime.now().timestamp()
            }

            passwordResetToken = encrypt(json.dumps(userData))

            passwordResetLink = ( str.encode(os.environ.get("CORS")) + b"/resetPassword?token=" + passwordResetToken).decode("utf-8")

            logger.info(passwordResetLink)
            sendMail(data['email'], 'Demande de changement de mot de passe', 'Vous avez demandé un changement de mot de passe. Si vous n\'avez pas fait cette requête, veuillez ignorer ce courriel.\n<a href="' + passwordResetLink + '" target="_blank">Appuyez</a>')
            return jsonify({'message': 'Successfully sent a password request'})
        else:
            logger.warn("A user tried to reset but provided a bad email")
            return jsonify({'message': 'The email provided is invalid (No user found/invalid)'}), 401
    except Exception as e:
        logger.warn("A user tried to send a reset password request but it failed")
        return jsonify({'Error while sending password request'}), 500
    

@user_blueprint.route('/resetPassword', methods=['POST'])
def resetPassword():
    try:
        data = request.get_json()
        decryptedData = json.loads(decrypt(data['token']))

        if data['password'] == data['confirmPassword']:
            try:
                if (decryptedData['resetDate'] + 900) > datetime.now().timestamp():
                    auth_repo.updatePassword(decryptedData['email'], data['password'])
                    return jsonify({'message': 'Successfully resetted the password'})
                else:
                    logger.warn("A user tried to reset the password via a expired link")
                    return jsonify({'message': 'Error while trying to reset the password (Link expired)'}), 403
            except Exception as e:
                logger.warn("A user tried to reset the password but it failed")
                return jsonify({'message': 'Error while trying to reset the password'}), 401
    except Exception as e:
        logger.warn("A user tried to use reset password with an invalid token")
        return jsonify({'message': 'Error while trying to reset the password, is token valid?'}), 403