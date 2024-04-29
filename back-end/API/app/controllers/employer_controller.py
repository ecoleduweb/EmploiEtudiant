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


@employer_blueprint.route('/createEmployer', methods=['POST'])
@token_admin_required
def createEmployer(current_user):
    data = request.get_json()
    employer = employer_service.createEmployer(data["enterpriseId"], data["userId"])
    return jsonify(employer.to_json_string())

@employer_blueprint.route('/getEmployer', methods=['GET'])
@token_required
def getEmployer(current_user):
    id = request.args.get('id')
    employer = employer_service.getEmployer(id)
    if employer:
        return jsonify(employer.to_json_string())
    else:
        return jsonify({'message': 'employer not found'})
    
@employer_blueprint.route('/linkEmployerEnterprise', methods=['PUT'])
@token_required
def linkEmployerEnterprise(current_user):
    data = request.get_json()
    return employer_service.linkEmployerEnterprise(data)

@employer_blueprint.route('/updateEmployer', methods=['PUT'])
@token_admin_required
def updateEmployer(current_user):
    id = request.args.get('id')
    employer = employer_service.getEmployer(id)
    if employer:
        data = request.get_json()
        employer_service.updateEmployer(data, id)
        return jsonify({'message': 'employer updated'})
    else:
        return jsonify({'message': 'employer not found'})
    
@employer_blueprint.route('/deleteEmployer', methods=['DELETE'])
@token_admin_required
def deleteEmployer(current_user):
    id = request.args.get('id')
    employer = employer_service.getEmployer(id)
    if employer:
        employer_service.deleteEmployer(id)
        return jsonify({'message': 'employer deleted'})
    else:
        return jsonify({'message': 'employer not found'})