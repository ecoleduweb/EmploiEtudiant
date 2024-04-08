from app.repositories.employer_repo import EmployerRepo
employer_repo = EmployerRepo()

class EmployerService:
    def createEmployer(self, enterpriseId, userId):
        return employer_repo.createEmployer(enterpriseId, userId)

    def linkEmployerEnterprise(self, data):
        return employer_repo.linkEmployerEnterprise(data)