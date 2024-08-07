from flask import jsonify, request, Blueprint
from app.models.region_model import Region
from app.services.city_service import CityService
from app.middleware.tokenVerify import token_required
from logging import getLogger

logger = getLogger(__name__)
city_blueprint = Blueprint('city', __name__)
city_service = CityService()

@city_blueprint.route('/<int:id>', methods=['GET'])
def oneCity(id):
    if not id:
        logger.warning('no city_id provided')
        return jsonify({'message': 'no id provided'}), 400
    city = city_service.oneCity(id)
    if not city:
        logger.warning('no city found for id : ' + id + ' in the database')
        return jsonify({'message': 'no city found'}), 404
    region = Region.query.filter_by(id=city.idRegion).first()
    return jsonify({'id': city.id, 'city': city.city, 'region': region.region})

@city_blueprint.route('/all', methods=['GET'])
def allCities():
    cities = city_service.allCities()
    if not cities:
        logger.warning('no cities found in the database')
        return jsonify({'message': 'no cities found'}), 404
    cities_list = []
    
    # ACM : Si on est en mesure d'utiliser l'ORM de façon efficace, on pourra faire le join dans la bd directement.
    for city in cities:
        region = Region.query.filter_by(id=city.idRegion).first()
        cities_list.append({'id': city.id, 'city': city.city, 'region': region.region})
    return jsonify(cities_list)