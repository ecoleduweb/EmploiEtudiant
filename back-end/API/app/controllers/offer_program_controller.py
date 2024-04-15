from flask import jsonify, request, Blueprint
from app.services.offer_program_service import OfferProgramService
from app.middleware.tokenVerify import token_required
offer_program_service = OfferProgramService()

offer_program_blueprint = Blueprint('offerProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@token_required
@offer_program_blueprint.route('/linkOfferProgram', methods=['POST'])
def linkOfferProgram():
    data = request.get_json()
    offerProgram = offer_program_service.linkOfferProgram(data["offerId"], data["studyProgramId"])
    return (jsonify(offerProgram.to_json_string()), 200)