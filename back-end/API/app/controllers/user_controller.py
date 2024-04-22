from flask import jsonify, request, Blueprint
from app.models.user_model import User
import os
from logging import getLogger
from jwt import decode
from flask import jsonify, request
from functools import wraps
from app.services.user_service import UserService
user_service = UserService()
from app.services.employer_service import EmployerService
employer_service = EmployerService()
from app.services.enterprise_service import EnterpriseService
enterprise_service = EnterpriseService()

logger = getLogger(__name__)
user_blueprint = Blueprint('user', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            if not token:
                logger.warn('A valid token is missing')
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = User.query.filter_by(email = data['email']).first()

            except Exception as e:
                print(e)
                logger.warn('Token is invalid')
                return jsonify({'message': 'token is invalid'})
            return f(current_user)
        return decorated

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return user_service.login(data["email"], data["password"])

@user_blueprint.route('/createUser', methods=['POST'])
def createUser():
    data = request.get_json()
    if not all([data.get('id'), data.get('email'), data.get('password')]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if not isinstance(data, dict):
        logger.warn('Invalid JSON data format in /createUser')
        return jsonify({'message': 'Invalid JSON data format'}), 400

    if user_service.getUser(data['email']) is not None:
        return jsonify({'message': 'User already exists'}), 400

    return user_service.createUser(data)

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
        return jsonify({'message': 'Missing required fields'}), 400
    
    logger.warn('Password updated for user: ' + email)
    return user_service.updatePassword(data)

@user_blueprint.route('/getAllUsers', methods=['GET'])
@token_required
def getAllUsers():
    logger.warn('All users retrieved')
    return user_service.getAllUsers()

@user_blueprint.route('/getUser', methods=['GET'])
@token_required
def getUser(current_user):
    logger.warn('Attempt to retrive user information of: ' + current_user.email)
    token = request.headers.get('Authorization')
    data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
    email = data['email']
    if not token:
        return jsonify({'message': 'Missing required fields'}), 400
    user = user_service.getUser(email)
    return jsonify(user.to_json_string())
