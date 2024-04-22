from flask import jsonify, request, Blueprint
from flask import Flask, jsonify, request, make_response
from app.services.enterprise_service import EnterpriseService
from app.services.employer_service import EmployerService
from app.middleware.adminTokenVerified import token_admin_required
enterprise_service = EnterpriseService()
employer_service = EmployerService()

enterprise_blueprint = Blueprint('enterprise', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@enterprise_blueprint.route('/createEnterprise', methods=['POST'])
@token_admin_required
def createEnterprise(current_user):
    data = request.get_json()
    entreprise = enterprise_service.createEnterprise(data, False)
    return jsonify({'message': 'Enterprise created successfully'})

@enterprise_blueprint.route('/getEntrepriseId', methods=['GET'])
@token_admin_required
def getEntrepriseId(current_user):
    name = request.args.get('name')
    return enterprise_service.getEntrepriseId(name)