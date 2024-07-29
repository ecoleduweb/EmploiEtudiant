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
                logger.warn('User not found with employer')
                return None
        else:
            logger.warn("Employer not found from enterprise")
            return None