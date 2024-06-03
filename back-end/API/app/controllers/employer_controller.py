from flask import jsonify, request, Blueprint
from app.services.employer_service import EmployerService
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required
from logging import getLogger
employer_service = EmployerService()

logger = getLogger(__name__)
employer_blueprint = Blueprint('employer', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@employer_blueprint.route('/new', methods=['POST'])
@token_admin_required
def createEmployer(current_user):
    data = request.get_json()
    employer = employer_service.createEmployer(data["enterpriseId"], data["userId"])
    return jsonify(employer.to_json_string())

@employer_blueprint.route('/<int:id>', methods=['GET'])
@token_required
def getEmployer(current_user, id):
    employer = employer_service.getEmployer(id)
    if employer:
        return jsonify(employer.to_json_string())
    else:
        logger.warn('Employer not found with id : ' + id)
        return jsonify({'message': 'employer not found'}), 404
    
@employer_blueprint.route('/linkEmployerEnterprise', methods=['PUT'])
@token_required
def linkEmployerEnterprise(current_user):
    data = request.get_json()
    return employer_service.linkEmployerEnterprise(data)

@employer_blueprint.route('/<int:id>', methods=['PUT'])
@token_admin_required
def updateEmployer(current_user, id):
    employer = employer_service.getEmployer(id)
    if employer:
        data = request.get_json()
        employer_service.updateEmployer(data, id)
        return jsonify({'message': 'employer updated'})
    else:
        logger.warn('Employer not found with id : ' + id)
        return jsonify({'message': 'employer not found'}), 404
    
@employer_blueprint.route('/currentEmployer', methods=['GET'])
@token_required
def getEmployerByUserId(current_user):
    employer = employer_service.getEmployerByUserId(current_user.id)
    if employer:
        return jsonify(employer.to_json_string())
    else:
        logger.warn(f'Current user with id {current_user.id} has no employer')
        return jsonify({'message': 'employer not found'}), 404
