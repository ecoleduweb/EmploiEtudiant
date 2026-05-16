from app.repositories.enterprise_repo import EnterpriseRepo
from app.models.enterprise_model import Enterprise
enterprise_repo = EnterpriseRepo()

class EnterpriseService:
    
    def getEnterprises(self):
        return enterprise_repo.getEnterprises()
    
    def getAllEmployersFromEntreprise(self, id):
        return enterprise_repo.getAllEmployersFromEntreprise(id)
    
    def createEnterprise(self, enterprise: Enterprise, isTemporary: bool):

        return enterprise_repo.createEnterprise(enterprise, isTemporary)
    
    def getEnterpriseByEmployer(self, employerId):
        return enterprise_repo.getEnterpriseByEmployer(employerId)
    
    def getEmployerFromEnterprise(self, id):
        return enterprise_repo.getEmployerFromEntreprise(self, id)

    def getEnterprise(self, id):
        return enterprise_repo.getEnterprise(id)
    
    def updateEnterprise(self, enterprise: Enterprise):
        current_employers = self.getAllEmployersFromEntreprise(enterprise.id) or []
        current_user_ids = [e.userId for e in current_employers]
        
        new_user_ids = enterprise.userIds or []

        user_ids_to_remove = [
            uid for uid in current_user_ids
            if uid not in new_user_ids
        ]
        if user_ids_to_remove:
            raise Exception("La suppression d'employeurs n'est pas encore supportée.")
        return enterprise_repo.updateEnterprise(enterprise)
    
    def deleteEnterprise(self, id):
        return enterprise_repo.deleteEnterprise(id)
    
    def getEnterpriseId(self, name):
        return enterprise_repo.getEnterpriseId(name)