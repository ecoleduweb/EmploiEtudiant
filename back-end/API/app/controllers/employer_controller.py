from flask import jsonify, request, Blueprint
from app.services.employer_service import EmployerService
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required
from app.controllers.email_controller import sendMail
import os
employer_service = EmployerService()

employer_blueprint = Blueprint('employer', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@employer_blueprint.route('/createEmployer', methods=['POST'])
@token_admin_required
def createEmployer(current_user):
    data = request.get_json()
    employer = employer_service.createEmployer(data["enterpriseId"], data["userId"])
    sendMail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Création d'un compte employeur", "Un nouveau compte employeur a été créé.")
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

@employer_blueprint.route('/getEmployerByEnterpriseId/<int:id>', methods=['GET'])
@token_admin_required
def getEmployerByEnterpriseId():
    id = request.args.get('id')
    return employer_service.getEmployerByEnterpriseId(id)

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

@employer_blueprint.route('/getEmployerByUserId', methods=['GET'])
@token_required
def getEmployerByUserId(current_user):
    id = request.args.get('id')
    if not id: id = current_user.id
    employer = employer_service.getEmployerByUserId(id)
    if employer:
        return jsonify(employer.to_json_string())
    else:
        return jsonify({'message': 'employer not found'}), 404
