from app.repositories.employer_repo import EmployerRepo
from app.repositories.enterprise_repo import EnterpriseRepo
from app.services.user_service import UserService
from logging import getLogger
employer_repo = EmployerRepo()
enterprise_repo = EnterpriseRepo()
user_service = UserService()

logger = getLogger(__name__)

class EmployerService:
    def createEmployer(self, enterpriseId, userId):
        return employer_repo.createEmployer(enterpriseId, userId)
    
    def getEmployer(self, id):
        return employer_repo.getEmployer(id)

    def updateEmployer(self, data, idEmployer):
        return employer_repo.updateEmployer(data, idEmployer)
    
    def deleteEmployer(self, id):
        return employer_repo.deleteEmployer(id)
    
    def getEmployerByUserId(self, userId):
        return employer_repo.getEmployerByUserId(userId)

    def getUserFromEmployer(self, id):
        employer = self.getEmployer(id)
        if(employer!=None):
            user = user_service.getUserById(employer.userId)
            if(user!=None):
                return user.email
            else:
                logger.warning('User not found with employer')
                return None
        else:
            logger.warning("Employer not found from enterprise")
            return None

    def getEmployersByEnterpriseId(self, enterpriseId):
        employers = employer_repo.getEmployersByEnterpriseId(enterpriseId)
        all_users = user_service.getAllUsers()
        users_dict = {user.id: user for user in all_users}
        
        enriched_employers = []
        for employer in employers:
            employer_data = employer.to_json_string()
            
            if employer.userId and employer.userId in users_dict:
                user = users_dict[employer.userId]
                employer_data['firstName'] = user.firstName
                employer_data['lastName'] = user.lastName
                employer_data['email'] = user.email
                employer_data['active'] = user.active
            else:
                employer_data['firstName'] = None
                employer_data['lastName'] = None
                employer_data['email'] = None
                employer_data['active'] = None
            
            enriched_employers.append(employer_data)
        
        return enriched_employers