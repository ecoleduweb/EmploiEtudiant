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
def getEnterpriseByEmployer():
    id = request.args.get('id')
    enterprise = enterprise_service.getEnterpriseByEmployer(id)
    if enterprise:
        return jsonify(enterprise.to_json_string()), 200
    else:
        logger.warn('Enterprise not found with id : ' + id)
        return jsonify({'message': 'enterprise not found'}), 404

@enterprise_blueprint.route('/updateEntreprise', methods=['PUT'])
@token_admin_required
def updateEntreprise(current_user):
    id = request.args.get('id')
    enterprise = enterprise_service.getEnterprise(id)
    if enterprise:
        data = request.get_json()
        enterprise_service.updateEnterprise(data)
        return jsonify({'message': 'enterprise updated'})
    else:
        logger.warn('Enterprise not found with id : ' + id)
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
            logger.warn('Enterprise with id ' + id + ' is not temporary and cannot be deleted')
            return jsonify({'message': 'enterprise is not temporary'})
    else:
        logger.warn('Enterprise not found with id : ' + id)
        return jsonify({'message': 'enterprise not found'})
    
@enterprise_blueprint.route('/getEntrepriseId', methods=['GET'])
@token_admin_required
def getEntrepriseId(current_user):
    name = request.args.get('name')
    return enterprise_service.getEntrepriseId(name)

@enterprise_blueprint.route('/getEnterprise', methods=['GET'])
@token_required
def getEnterprise(current_user):
    id = request.args.get('id')
    if id is None:
        logger.warn('ID is missing')
        return jsonify({'message': 'ID is missing'}), 400
    try:
        id = int(id)  # Convert the id to an integer
    except ValueError:
        logger.warn('ID must be an integer')
        return jsonify({'message': 'ID must be an integer'}), 400
    enterprise = enterprise_service.getEnterprise(id)
    if enterprise:
        return jsonify(enterprise.to_json_string()), 200
    else:
        logger.warn('Enterprise not found with id : ' + id)
        return jsonify({'message': 'enterprise not found'}), 404