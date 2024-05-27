from flask import jsonify, request, Blueprint
from app.services.offer_program_service import OfferProgramService
from app.middleware.tokenVerify import token_required
from logging import getLogger
offer_program_service = OfferProgramService()

logger = getLogger(__name__)
offer_program_blueprint = Blueprint('offerProgram', __name__) ## Représente l'app, https://flask.palletsprojects.com/en/2.2.x/blueprints/

@offer_program_blueprint.route('/<int:id>', methods=['GET'])
@token_required
def getProgramIdByOfferId(current_user, id):
    programs = offer_program_service.getProgramIdByOfferId(id)
    if programs:
        return jsonify(programs)
    else:
        logger.warn('No program found for the given offerId : ' + id)
        return jsonify({"error": "No program found for the given offerId"}), 404
    