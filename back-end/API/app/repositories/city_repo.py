from app.models.city_model import City

class CityRepo:

        def oneCity(self, id):
            city = City.query.filter_by(id=id).first()
            return city
    
        def allCities(self):
            cities = City.query.all()
            return cities