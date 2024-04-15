from flask import jsonify, request, Blueprint
from app.services.study_program_service import StudyProgramService
from app.middleware.tokenVerify import token_required
study_program_service = StudyProgramService()

study_program_blueprint = Blueprint('studyProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@token_required
@study_program_blueprint.route('/studyPrograms', methods=['GET'])
def studyPrograms():
    studyPrograms = study_program_service.studyPrograms()
    return jsonify(studyPrograms)

@token_required
@study_program_blueprint.route('/studyProgramId', methods=['GET'])
def studyProgramId():
    name = request.args.get('name')
    studyProgramId = study_program_service.studyProgramId(name)
    return jsonify(studyProgramId)

@token_required
@study_program_blueprint.route('/addStudyProgram', methods=['POST'])
def addStudyProgram():
    data = request.get_json()
    studyProgram = study_program_service.addStudyProgram(data["name"])
    return jsonify({'message': 'Study program added successfully'})