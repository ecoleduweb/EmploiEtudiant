from app.repositories.enterprise_repo import EnterpriseRepo
enterprise_repo = EnterpriseRepo()

class EnterpriseService:

    def getEnterprises(self):
        return enterprise_repo.getEnterprises()
    
    def createEnterprise(self, data, isTemporary):
        return enterprise_repo.createEnterprise(data, isTemporary)
    
    def getEnterpriseByEmployer(self, employerId):
        return enterprise_repo.getEnterpriseByEmployer(employerId)
    
    def updateEnterprise(self, data):
        return enterprise_repo.updateEnterprise(data)
    
    def deleteEnterprise(self, id):
        return enterprise_repo.deleteEnterprise(id)
    def getEntrepriseId(self, name):
        return enterprise_repo.getEntrepriseId(name)