from flask import jsonify, request, Blueprint
from app.services.employer_service import EmployerService
from app.middleware.tokenVerify import token_required
from app.middleware.adminTokenVerified import token_admin_required
employer_service = EmployerService()

employer_blueprint = Blueprint('employer', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@employer_blueprint.route('/createEmployer', methods=['POST'])
@token_admin_required
def createEmployer():
    data = request.get_json()
    return employer_service.createEmployer(data)
    
@employer_blueprint.route('/linkEmployerEnterprise', methods=['PUT'])
@token_required
def linkEmployerEnterprise():
    data = request.get_json()
    return employer_service.linkEmployerEnterprise(data)

@employer_blueprint.route('/getEmployerByEnterpriseId/<int:id>', methods=['GET'])
@token_admin_required
def getEmployerByEnterpriseId():
    id = request.args.get('id')
    return employer_service.getEmployerByEnterpriseId(id)