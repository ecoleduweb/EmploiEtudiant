from app.repositories.city_repo import CityRepo
city_repo = CityRepo()

class CityService:
    def oneCity(self, id):
        return city_repo.oneCity(id)
    
    def allCities(self):
        return city_repo.allCities()