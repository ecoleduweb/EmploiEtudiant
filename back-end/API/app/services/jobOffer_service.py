from app.repositories.jobOffer_repo import JobOfferRepo
jobOffer_repo = JobOfferRepo()

class JobOfferService:

    def createJobOffer(self, data, employerId):
        return jobOffer_repo.createJobOffer(data, employerId)

    def offreEmploi(self, data):
        return jobOffer_repo.offreEmploi(data)

    def offresEmploi(self):
        return jobOffer_repo.offresEmploi()
    
    def linkJobOfferEmployer(self, data):
        return jobOffer_repo.linkJobOfferEmployer(data)