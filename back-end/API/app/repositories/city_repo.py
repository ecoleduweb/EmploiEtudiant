from app.models.city_model import City
from app.dtos.city_dto import CityReadDTO
from app.customexception.exception import  NotFoundException

class CityRepo:

    def find_by_id(self, id):
        city = City.query.filter_by(id=id).first()
        if (not city):
            raise NotFoundException('No city found for id : ', id)
        return CityReadDTO.model_validate(city)

    def find_all(self):
        cities = City.query.all()
        return [CityReadDTO.model_validate(city) for city in cities]