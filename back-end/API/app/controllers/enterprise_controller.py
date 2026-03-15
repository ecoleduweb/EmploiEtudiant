from flask import jsonify, request, Blueprint
from flask import Flask, jsonify, request, make_response
from app.services.enterprise_service import EnterpriseService
from app.services.employer_service import EmployerService
from app.services.user_service import UserService
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
        logger.warning('Enterprise not found with id : ' + str(id))
        return jsonify({'message': 'enterprise not found'}), 404

@enterprise_blueprint.route('/<int:id>', methods=['PUT'])
@token_required
def updateEnterprise(current_user, id):
    try:
        data = request.get_json()

        if current_user.isModerator and data.get("id") is not None:
            enterprise = enterprise_service.getEnterprise(data["id"])
            if enterprise:
                enterprise_service.updateEnterprise(data)
                return jsonify({'message': 'enterprise updated'})
            else:
                logger.warning(f'Enterprise not found with id : {data["id"]}')
                return jsonify({'message': 'enterprise not found'}), 404
        else:
            employer = employer_service.getEmployerByUserId(current_user.id)
            if not employer:
                logger.warning("User has no associated employer")
                return jsonify({'message': 'User has no associated employer'}), 403
                
            enterprise = enterprise_service.getEnterprise(employer.enterpriseId)
            if not enterprise:
                logger.warning(f'Enterprise not found for employer with enterpriseId: {employer.enterpriseId}')
                return jsonify({'message': 'enterprise not found'}), 404
            data["id"] = enterprise.id
            if enterprise and enterprise.id == data["id"]:
                enterprise_service.updateEnterprise(data)
                return jsonify({'message': 'enterprise updated'})
            else:
                logger.warning("An user tried to modify an entreprise don't have permission")
                return jsonify({'message': 'User cannot modify enterprise'}), 401
            
    except Exception as e:
        logger.exception(f'There was an error updating the enterprise')
        return jsonify({'message': 'There was an error updating the enterprise'}), 500

@enterprise_blueprint.route('/<int:id>', methods=['GET'])
@token_required
def getEnterprise(current_user, id):
    enterprise = enterprise_service.getEnterprise(id)
    if enterprise:
        return jsonify(enterprise.to_json_string()), 200
    else:
        logger.warning(f'Enterprise not found with id : {id}')
        return jsonify({'message': 'enterprise not found'}), 404
    
@enterprise_blueprint.route('/currentEnterprise', methods=['GET'])
@token_required
def getCurrentUserEnterprise(current_user):
    try:
        employer = employer_service.getEmployerByUserId(current_user.id)
        if employer:
            enterprise = enterprise_service.getEnterprise(employer.enterpriseId)
        else:
            logger.info("Couldn't get the current user to get the enterprise")
            return jsonify({'message': 'Couldn\'t get the user'}), 404
        if enterprise:
            return jsonify(enterprise.to_json_string()), 200
        else:
            logger.warning("No enterprise found the current user")
            return jsonify({'message': 'No enterprise found on the current user'}), 404
    except Exception as e:
        logger.exception("Error getting the user to get the enterprise")
        return jsonify({'message': 'Error when getting the user'}), 500
