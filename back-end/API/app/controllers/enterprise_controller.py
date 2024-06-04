from flask import jsonify, request, Blueprint
from flask import Flask, jsonify, request, make_response
from app.services.enterprise_service import EnterpriseService
from app.services.employer_service import EmployerService
from app.middleware.adminTokenVerified import token_admin_required
from app.middleware.tokenVerify import token_required
from logging import getLogger
enterprise_service = EnterpriseService()
employer_service = EmployerService()

logger = getLogger(__name__)
enterprise_blueprint = Blueprint('enterprise', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@enterprise_blueprint.route('/all', methods=['GET'])
@token_admin_required
def getEnterprises(current_user):
    enterprises = enterprise_service.getEnterprises()
    return jsonify([enterprise.to_json_string() for enterprise in enterprises])

@enterprise_blueprint.route('/new', methods=['POST'])
@token_admin_required
def createEnterprise(current_user):
    enterpriseToCreate = request.get_json()
    createdEnterprise = enterprise_service.createEnterprise(enterpriseToCreate, False)
    return jsonify(createdEnterprise.to_json_string())

@enterprise_blueprint.route('/employer/<int:id>', methods=['GET'])
def getEnterpriseByEmployer(id):
    enterprise = enterprise_service.getEnterpriseByEmployer(id)
    if enterprise:
        return jsonify(enterprise.to_json_string()), 200
    else:
        logger.warn('Enterprise not found with id : ' + id)
        return jsonify({'message': 'enterprise not found'}), 404

@enterprise_blueprint.route('/<int:id>', methods=['PUT'])
@token_admin_required
def updateEnterprise(current_user, id):
    enterprise = enterprise_service.getEnterprise(id)
    if enterprise:
        data = request.get_json()
        enterprise_service.updateEnterprise(data)
        return jsonify({'message': 'enterprise updated'})
    else:
        logger.warn('Enterprise not found with id : ' + id)
        return jsonify({'message': 'enterprise not found'})

@enterprise_blueprint.route('/<int:id>', methods=['GET'])
@token_required
def getEnterprise(current_user, id):
    enterprise = enterprise_service.getEnterprise(id)
    if enterprise:
        return jsonify(enterprise.to_json_string()), 200
    else:
        logger.warn('Enterprise not found with id : ' + id)
        return jsonify({'message': 'enterprise not found'}), 404