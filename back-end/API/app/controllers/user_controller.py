from flask import jsonify, request, Blueprint
import os
from logging import getLogger
from jwt import decode
from app.services.user_service import UserService
from app.services.employer_service import EmployerService
from app.services.enterprise_service import EnterpriseService
from app.middleware.tokenVerify import token_required
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
    if not all([data.get('email'), data.get('password'), data.get('firstName'), data.get('lastName')]):
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
def updatePassword():
    data = request.get_json()
    if not isinstance(data, dict):
        logger.warn('Invalid JSON data format in /updatePassword')
        return jsonify({'message': 'Invalid JSON data format'}), 400
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        logger.warn('Missing required fields in /updatePassword : \nEmail :' + email + ' \nPassword : ' + password)
        return jsonify({'message': 'Missing required fields'}), 400
    
    return user_service.updatePassword(data)

@user_blueprint.route('/getAllUsers', methods=['GET'])
@token_required
def getAllUsers():
    return user_service.getAllUsers()

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
