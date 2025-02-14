from app.repositories.jobOffer_repo import JobOfferRepo
from app.repositories.enterprise_repo import EnterpriseRepo
from app.repositories.study_program_repo import StudyProgramRepo
from app.models.jobOffer_model import JobOffer
from app.models.JobOffer_details import JobOfferDetails
from datetime import datetime
from app.middleware.lengthVerify import verifyStringLen
from app.customexception.CustomException import NotFoundException
jobOffer_repo = JobOfferRepo()
enterprise_repo = EnterpriseRepo()
studyProgram_repo = StudyProgramRepo()
class JobOfferService:

    def offresEmploi(self, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails):
        return jobOffer_repo.offresEmploi(needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
    
    def createJobOffer(self, data, employerId, isApproved, last_modified_by_id):

        verifyStringLen(data['title'], 255)
        verifyStringLen(data['address'], 255)
        verifyStringLen(data['email'], 255)
        verifyStringLen(data['offerLink'], 255)
        verifyStringLen(data['salary'], 255)

        new_job_offer = JobOffer(title=data['title'],
         description=data['description'],
         offerDebut=data["offerDebut"],
         address=data['address'],
         dateEntryOffice=data['dateEntryOffice'],
         deadlineApply=data['deadlineApply'],
         email=data['email'],
         hoursPerWeek=data['hoursPerWeek'],
         offerLink=data['offerLink'],
         salary=data['salary'],
         active=data['active'],
         employerId=employerId,
         isApproved=isApproved,
         approvedDate=datetime.now() if isApproved else None,
         last_modified_by_id=last_modified_by_id)

        return jobOffer_repo.createJobOffer(new_job_offer)
    
    def offresEmploiEmployeur(self, employerId, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails):
        return jobOffer_repo.offresEmploiEmployeur(employerId, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
    
    def updateJobOffer(self, data):
        return jobOffer_repo.updateJobOffer(data)

    def findById(self, id):
        return jobOffer_repo.offreEmploi(id)

    def getOffers(self, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails):
        return jobOffer_repo.getOffers(getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
    
    def getRecentOffers(self, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails):
        return jobOffer_repo.getRecentOffers(getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
    
    def linkJobOfferEmployer(self, data):
        return jobOffer_repo.linkJobOfferEmployer(data)
    
    def approveJobOffer(self, id, isApproved, approbationMessage):
        return jobOffer_repo.approveJobOffer(id, isApproved, approbationMessage)
    
    def archiveJobOffer(self, id):
        if jobOffer_repo.jobOfferExist(id):
            jobOffer_repo.archiveJobOffer(id)
    
    def getInfo(self, jobOfferModel, entrepriseDetails, employmentScheduleDetails, studyProgramDetails):
        jobOfferDetails = JobOfferDetails(jobOfferModel)

        # Créer un objet jobOfferDetails et y passer le jobOffer dans le constructeur.

        if entrepriseDetails != None and entrepriseDetails:
            enterprise = enterprise_repo.getEnterpriseByEmployerId(jobOfferModel.employerId)
            jobOfferDetails.AddEnterprise(enterprise)
    
        if employmentScheduleDetails != None and employmentScheduleDetails:
            print("Employment schedule")

        #if studyProgramDetails != None and studyProgramDetails:
        #    jobOfferDetails["studyProgram"] = studyPrograms
        
        return jobOfferDetails