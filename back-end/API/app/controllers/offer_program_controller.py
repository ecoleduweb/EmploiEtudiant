from flask import jsonify, request, Blueprint
import os
from app import db
from app.models.user_model import User
from app.models.offer_programm_model import OfferProgram
import os
from jwt import decode
from flask import jsonify, request
from functools import wraps
from app.services.offer_program_service import OfferProgramService
offer_program_service = OfferProgramService()


offer_program_blueprint = Blueprint('offerProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

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
@offer_program_blueprint.route('/linkOfferProgram', methods=['POST'])
def linkOfferProgram():
    data = request.get_json()
    offerProgram = offer_program_service.linkOfferProgram(data["offerId"], data["studyProgramId"])
    return (jsonify(offerProgram.to_json_string()), 200)