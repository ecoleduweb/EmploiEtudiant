from app.repositories.jobOffer_repo import JobOfferRepo
jobOffer_repo = JobOfferRepo()

class JobOfferService:

    def offresEmploi(self):
        return jobOffer_repo.offresEmploi()
    
    def createJobOffer(self, data, employerId, isApproved):
        return jobOffer_repo.createJobOffer(data, employerId, isApproved)
    
    def offresEmploiEmployeur(self, employerId):
        return jobOffer_repo.offresEmploiEmployeur(employerId)
    
    def updateJobOffer(self, data):
        return jobOffer_repo.updateJobOffer(data)

    def findById(self, id):
        return jobOffer_repo.offreEmploi(id)

    def offresEmploiApproved(self):
        return jobOffer_repo.offresEmploiApproved()
    
    def linkJobOfferEmployer(self, data):
        return jobOffer_repo.linkJobOfferEmployer(data)
    
    def approveJobOffer(self, data):
        return jobOffer_repo.approveJobOffer(data)
    