from flask import jsonify, request, Blueprint
from app.services.offer_program_service import OfferProgramService
from app.middleware.tokenVerify import token_required
offer_program_service = OfferProgramService()

offer_program_blueprint = Blueprint('offerProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@offer_program_blueprint.route('/linkOfferProgram', methods=['POST'])
@token_required
def linkOfferProgram(current_user):
    data = request.get_json()
    offerProgram = offer_program_service.linkOfferProgram(data["offerId"], data["studyProgramId"])
    return (jsonify(offerProgram.to_json_string()), 200)

@offer_program_blueprint.route('/getProgramIdByOfferId', methods=['GET'])
@token_required
def getProgramIdByOfferId(current_user):
    offerId = request.args.get('offerId')
    if not offerId:
        return jsonify({"error": "offerId is required"}), 400
    programId = offer_program_service.getProgramIdByOfferId(offerId)
    if programId:
        return jsonify(programId)
    else:
        return jsonify({"error": "No program found for the given offerId"}), 404