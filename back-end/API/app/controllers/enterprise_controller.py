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
@enterprise_blueprint.route('/getEnterprises', methods=['GET'])
def getEnterprises():
    enterprises = enterprise_service.getEnterprises()
    return jsonify([enterprise.to_json_string() for enterprise in enterprises])

@token_admin_required
@enterprise_blueprint.route('/createEnterprise', methods=['POST'])
def createEnterprise():
    data = request.get_json()
    enterprise = enterprise_service.createEnterprise(data, False)
    return jsonify(enterprise.to_json_string())

@token_admin_required
@enterprise_blueprint.route('/updateEntreprise/<idEnterprise>', methods=['PUT'])
def updateEntreprise(idEnterprise):
    enterprise = enterprise_service.getEnterprise(idEnterprise)
    if enterprise:
        data = request.get_json()
        enterprise_service.updateEnterprise(data)
        print('test')
        return jsonify({'message': 'enterprise updated'})
    else:
        return jsonify({'message': 'enterprise not found'})

@token_admin_required
@enterprise_blueprint.route('/deleteEnterprise/<idEnterprise>', methods=['DELETE'])
def deleteEnterprise(idEnterprise):
    enterprise = enterprise_service.getEnterprise(idEnterprise)
    if enterprise:
        if enterprise_service.deleteEnterprise(idEnterprise):
            return jsonify({'message': 'enterprise deleted'})
        else:
            return jsonify({'message': 'enterprise is not temporary'})
    else:
        return jsonify({'message': 'enterprise not found'})