from flask import jsonify, request, Blueprint
from app.models.region_model import Region
from app.services.city_service import CityService
from app.middleware.tokenVerify import token_required
from logging import getLogger

logger = getLogger(__name__)
city_blueprint = Blueprint('city', __name__)
city_service = CityService()

@city_blueprint.route('/oneCity', methods=['GET'])
@token_required
def oneCity(self):
    city_id = request.args.get('id')
    if not city_id:
        logger.warn('no city_id provided')
        return jsonify({'message': 'no id provided'}), 400
    city = city_service.oneCity(city_id)
    if not city:
        logger.warn('no city found for id : ' + city_id + ' in the database')
        return jsonify({'message': 'no city found'}), 404
    region = Region.query.filter_by(id=city.idRegion).first()
    return jsonify({'id': city.id, 'city': city.city, 'region': region.region})

@city_blueprint.route('/allCities', methods=['GET'])
@token_required
def allCities(self):
    cities = city_service.allCities()
    if not cities:
        logger.warn('no cities found in the database')
        return jsonify({'message': 'no cities found'}), 404
    cities_list = []
    for city in cities:
        region = Region.query.filter_by(id=city.idRegion).first()
        cities_list.append({'id': city.id, 'city': city.city, 'region': region.region})
    return jsonify(cities_list)