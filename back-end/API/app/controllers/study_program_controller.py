from flask import jsonify, request, Blueprint
from app.services.study_program_service import StudyProgramService
from app.middleware.tokenVerify import token_required
study_program_service = StudyProgramService()

study_program_blueprint = Blueprint('studyProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@study_program_blueprint.route('/studyPrograms', methods=['GET'])
@token_required
def studyPrograms():
    studyPrograms = study_program_service.studyPrograms()
    return jsonify(studyPrograms)

@study_program_blueprint.route('/studyProgramId', methods=['GET'])
@token_required
def studyProgramId():
    name = request.args.get('name')
    studyProgramId = study_program_service.studyProgramId(name)
    return jsonify(studyProgramId)

@study_program_blueprint.route('/addStudyProgram', methods=['POST'])
@token_required
def addStudyProgram():
    data = request.get_json()
    studyProgram = study_program_service.addStudyProgram(data["name"])
    return jsonify({'message': 'Study program added successfully'})