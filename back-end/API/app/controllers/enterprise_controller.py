from flask import jsonify, request, Blueprint
from app.models.jobOffer_model import JobOffer
import os
from app.models.user_model import User
import os
from jwt import decode
from flask import Flask, jsonify, request, make_response
from functools import wraps
from app.services.enterprise_service import EnterpriseService
enterprise_service = EnterpriseService()
from app.services.employer_service import EmployerService
employer_service = EmployerService()

enterprise_blueprint = Blueprint('enterprise', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

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

@enterprise_blueprint.route('/getEnterprises', methods=['GET'])
@token_admin_required
def getEnterprises(current_user):
    enterprises = enterprise_service.getEnterprises()
    return jsonify([enterprise.to_json_string() for enterprise in enterprises])

@enterprise_blueprint.route('/createEnterprise', methods=['POST'])
@token_admin_required
def createEnterprise(current_user):
    data = request.get_json()
    enterprise = enterprise_service.createEnterprise(data, False)
    return jsonify(enterprise.to_json_string())

@enterprise_blueprint.route('/getEnterpriseByEmployer', methods=['GET'])
@token_required
def getEnterpriseByEmployer(current_user):
    id = request.args.get('id')
    enterprise = enterprise_service.getEnterpriseByEmployer(id)
    if enterprise:
        return jsonify(enterprise.to_json_string()), 200
    else:
        return jsonify({'message': 'enterprise not found'}), 404

@enterprise_blueprint.route('/updateEntreprise', methods=['PUT'])
@token_admin_required
def updateEntreprise(current_user):
    id = request.args.get('id')
    enterprise = enterprise_service.getEnterprise(id)
    if enterprise:
        data = request.get_json()
        enterprise_service.updateEnterprise(data)
        print('test')
        return jsonify({'message': 'enterprise updated'})
    else:
        return jsonify({'message': 'enterprise not found'})

@enterprise_blueprint.route('/deleteEnterprise', methods=['DELETE'])
@token_admin_required
def deleteEnterprise(current_user):
    id = request.args.get('id')
    enterprise = enterprise_service.getEnterprise(id)
    if enterprise:
        if enterprise_service.deleteEnterprise(id):
            return jsonify({'message': 'enterprise deleted'})
        else:
            return jsonify({'message': 'enterprise is not temporary'})
    else:
        return jsonify({'message': 'enterprise not found'})
    
@enterprise_blueprint.route('/getEntrepriseId', methods=['GET'])
@token_admin_required
def getEntrepriseId(current_user):
    name = request.args.get('name')
    return enterprise_service.getEntrepriseId(name)