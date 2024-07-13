from flask import jsonify, request, Blueprint
import os
from logging import getLogger
from jwt import decode
from app.services.user_service import UserService
from app.services.employer_service import EmployerService
from app.services.enterprise_service import EnterpriseService
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required

user_service = UserService()
employer_service = EmployerService()
enterprise_service = EnterpriseService()
from logging import getLogger

logger = getLogger(__name__)
user_blueprint = Blueprint('user', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return user_service.login(data["email"], data["password"])

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
