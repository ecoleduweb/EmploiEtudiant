from flask import jsonify, request, Blueprint
from app.services.study_program_service import StudyProgramService
from app.middleware.adminTokenVerified import token_admin_required
from app.middleware.tokenVerify import token_required
study_program_service = StudyProgramService()

study_program_blueprint = Blueprint('studyProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

#ACM il faudra utiliser ce controlleur lorsque la gestion des programmes sera mise en place. Il faudra aussi la tester adéquatement

@study_program_blueprint.route('/studyPrograms', methods=['GET'])
@token_required
def studyPrograms(current_user):
    print("test")
    print(current_user)
    studyPrograms = study_program_service.studyPrograms()
    return jsonify(studyPrograms)

@study_program_blueprint.route('/studyProgram/<string:id>', methods=['GET'])
@token_required
def studyProgramId(current_user,name):
    studyProgramId = study_program_service.studyProgramId(name)
    return jsonify(studyProgramId)

@study_program_blueprint.route('/addStudyProgram', methods=['POST'])
@token_admin_required
def addStudyProgram(current_user):
    data = request.get_json()
    studyProgram = study_program_service.addStudyProgram(data["name"])
    return jsonify({'message': 'Study program added successfully'})