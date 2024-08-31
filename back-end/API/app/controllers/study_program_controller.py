import locale
from flask import jsonify, request, Blueprint
from app.services.study_program_service import StudyProgramService
from app.middleware.adminTokenVerified import token_admin_required
from app.middleware.tokenVerify import token_required
from app.customexception.CustomException import NotFoundException
from logging import getLogger
logger = getLogger(__name__)
study_program_service = StudyProgramService()

study_program_blueprint = Blueprint('studyProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8') # Set locale to french (Permet de trier correctement avec les accents...)

@study_program_blueprint.route('/studyPrograms', methods=['GET'])
def studyPrograms():
    studyPrograms = study_program_service.studyPrograms()
    sortedStudyPrograms = sorted(studyPrograms, key=lambda program: locale.strxfrm(program['name']))
    return jsonify(sortedStudyPrograms)

@study_program_blueprint.route('/studyProgram/<int:id>', methods=['PUT'])
@token_admin_required
def editStudyProgram(current_user, id):
    try:
        data = request.get_json()
        study_program_service.editStudyProgram(id, data["name"])
        return jsonify({'message': 'Study program edited successfully'})
    except NotFoundException as e:
        logger.warning("Couldn't edit study with id: " + str(id))
        return jsonify({'message': 'An error occured.'}), e.errorCode
    

    
@study_program_blueprint.route('/new', methods=['POST'])
@token_admin_required
def addStudyProgram(current_user):
    try:
        data = request.get_json()
        study_program_service.addStudyProgram(data["name"])
        return jsonify({'message': 'Study program added successfully'})
    except Exception as e:
        logger.warning("Couldn't add study with name: " + str(data["name"]))
        return jsonify({'message', 'An error occured.'}), 500