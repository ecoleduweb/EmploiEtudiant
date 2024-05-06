from flask import jsonify, request, Blueprint
import os
from logging import getLogger
from jwt import decode
import requests
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
    logger.info('Attempt to login on user with email: ' + data['email'])
    return user_service.login(data["email"], data["password"])

@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    logger.info('Attempt to create a new user with email: ' + data['email'])
    if not all([data.get('email'), data.get('password'), data.get('firstName'), data.get('lastName')]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if not isinstance(data, dict):
        logger.warn('Invalid JSON data format in /register')
        return jsonify({'message': 'Invalid JSON data format'}), 400

    if user_service.getUser(data['email']) == "<Response 29 bytes [200 OK]>" or user_service.getUser(data['email']) is not None:
        return jsonify({'message': 'User already exists'}), 400

    return user_service.register(data)

@user_blueprint.route('/updatePassword', methods=['PUT'])
@token_required
def updatePassword():
    data = request.get_json()
    logger.info('Attempt to update password on user with email: ' + data['email'])
    if not isinstance(data, dict):
        logger.warn('Invalid JSON data format in /updatePassword')
        return jsonify({'message': 'Invalid JSON data format'}), 400
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    logger.warn('Password updated for user: ' + email)
    return user_service.updatePassword(data)

@user_blueprint.route('/getAllUsers', methods=['GET'])
@token_required
def getAllUsers():
    logger.log('All users retrieved')
    return user_service.getAllUsers()

@user_blueprint.route('/getUser', methods=['GET'])
@token_required
def getUser(current_user):
    logger.warn('Attempt to retrive user information of: ' + current_user.email)
    token = request.headers.get('Authorization')
    data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    email = data['email']
    logger.warn('Attempt to retrive user information of: ' + email)
    if not token:
        return jsonify({'message': 'Missing required fields'}), 400
    user = user_service.getUser(email)
    return jsonify(user.to_json_string())

@user_blueprint.route('/verifyRecaptcha', methods=['POST'])
def verify_recaptcha(token):
    key = os.environ.get('RECAPTCHA_KEY')
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        "secret": key,
        "response": token
    }
    
    response = requests.post(url, data=params)
    result = response.json()
    
    if result['success'] and result['score'] >= 0.5:
        return True
    else:
        return False