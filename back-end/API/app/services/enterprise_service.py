from app.repositories.enterprise_repo import EnterpriseRepo
enterprise_repo = EnterpriseRepo()

class EnterpriseService:
    def createEnterprise(self, data, isTemporary):
        return enterprise_repo.createEnterprise(data, isTemporary)

    def getEntrepriseId(self, name):
        return enterprise_repo.getEntrepriseId(name)