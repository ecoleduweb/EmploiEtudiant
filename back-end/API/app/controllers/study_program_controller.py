from flask import jsonify, request, Blueprint
from app.services.study_program_service import StudyProgramService
from app.middleware.adminTokenVerified import token_admin_required
from app.middleware.tokenVerify import token_required
study_program_service = StudyProgramService()

study_program_blueprint = Blueprint('studyProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

#ACM il faudra utiliser ce controlleur lorsque la gestion des programmes sera mise en place. Il faudra aussi la tester adéquatement

@study_program_blueprint.route('/studyPrograms', methods=['GET'])
def studyPrograms():
    studyPrograms = study_program_service.studyPrograms()
    return jsonify(studyPrograms)

@study_program_blueprint.route('/editStudyProgram/<int:id>', methods=['POST'])
@token_admin_required
def editStudyProgram(current_user, id):
    try:
        data = request.get_json()
        study_program_service.editStudyProgram(id, data["name"])
        return jsonify({'message': 'Study program edited successfully'})
    except Exception as e:
        return jsonify({'message': 'An error occured.'}), 500
    

    
@study_program_blueprint.route('/addStudyProgram', methods=['POST'])
@token_admin_required
def addStudyProgram(current_user):
    data = request.get_json()
    studyProgram = study_program_service.addStudyProgram(data["name"])
    return jsonify({'message': 'Study program added successfully'})