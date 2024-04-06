from flask import jsonify, request, Blueprint
import os
from app import db
from app.models.user_model import User
from app.models.study_program_model import StudyProgram
import os
from jwt import decode
from flask import jsonify, request
from functools import wraps
from app.services.study_program_service import StudyProgramService
study_program_service = StudyProgramService()

study_program_blueprint = Blueprint('studyProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
                current_user = User.query.filter_by(email = data['email']).first()

            except Exception as e:
                print(e)
                return jsonify({'message': 'token is invalid'})
            return f(current_user)
        return decorated

@token_required
@study_program_blueprint.route('/studyPrograms', methods=['GET'])
def studyPrograms():
    studyPrograms = study_program_service.getStudyPrograms()
    return jsonify(studyPrograms)

@token_required
@study_program_blueprint.route('/studyProgramId', methods=['GET'])
def studyProgramId():
    data = request.get_json()
    studyProgramId = study_program_service.studyProgramId(data["name"])
    return jsonify(studyProgramId)

@token_required
@study_program_blueprint.route('/addStudyProgram', methods=['POST'])
def addStudyProgram():
    data = request.get_json()
    studyProgram = study_program_service.addStudyProgram(data)
    return jsonify({'message': 'Study program added successfully'})