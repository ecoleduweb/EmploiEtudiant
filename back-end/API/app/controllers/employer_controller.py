from flask import jsonify, request, Blueprint
import os
from app.models.user_model import User
import os
from jwt import decode
from flask import jsonify, request
from functools import wraps
from app.services.employer_service import EmployerService
employer_service = EmployerService()

employer_blueprint = Blueprint('employer', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = User.query.filter_by(email = data['email']).first()

            except Exception as e:
                print(e)
                return jsonify({'message': 'token is invalid'})
            return f(current_user)
        return decorated

def token_admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = User.query.filter_by(email = data['email']).first()

            except Exception as e:
                print(e)
                return jsonify({'message': 'token is invalid'})
            if current_user.isModerator:
                return f(current_user)
            else:
                return jsonify({'message': 'user is not admin'})
        return decorated

@token_admin_required
@employer_blueprint.route('/createEmployer', methods=['POST'])
def createEmployer():
    data = request.get_json()
    return employer_service.createEmployer(data)
    
@token_required
@employer_blueprint.route('/linkEmployerEnterprise', methods=['PUT'])
def linkEmployerEnterprise():
    data = request.get_json()
    return employer_service.linkEmployerEnterprise(data)