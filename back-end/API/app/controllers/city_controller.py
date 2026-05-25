from flask import jsonify, request, Blueprint
from app.models.region_model import Region
from app.services.city_service import CityService
from app.middleware.tokenVerify import token_required
from logging import getLogger
from app.dtos.city_dto import CityReadDTO

logger = getLogger(__name__)
city_blueprint = Blueprint('city', __name__)
city_service = CityService()

@city_blueprint.route('/<int:id>', methods=['GET'])
def oneCity(id):
    return city_service.oneCity(id).model_dump(), 200

@city_blueprint.route('/all', methods=['GET'])
def allCities():
    cities = city_service.allCities()
    return [city.model_dump() for city in cities], 200