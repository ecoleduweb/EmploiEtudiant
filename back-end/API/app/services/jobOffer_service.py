from app.repositories.jobOffer_repo import JobOfferRepo
from app.repositories.enterprise_repo import EnterpriseRepo
from app.repositories.study_program_repo import StudyProgramRepo
from app.models.jobOffer_model import JobOffer
from app.models.JobOffer_details import JobOfferDetails
from datetime import datetime
from app.middleware.lengthVerify import verifyStringLen
from app.middleware.numberVerify import verifyNumber
from app.customexception.CustomException import ValidationException
import re
jobOffer_repo = JobOfferRepo()
enterprise_repo = EnterpriseRepo()
studyProgram_repo = StudyProgramRepo()
class JobOfferService:

    def validateJobOffer(self, data, employerId, isApproved, last_modified_by_id):
        verifyStringLen('title', data['title'], 255)
        verifyStringLen('address', data['address'], 255)
        verifyStringLen('email', data['email'], 255)
        verifyStringLen('offerLink', data['offerLink'], 255)
        verifyStringLen('salary', data['salary'], 255)
        verifyNumber('hoursPerWeek', data['hoursPerWeek'], [float, int])
        if not (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', data['email'])):
            raise ValidationException('email', 'Le format du courriel est invalide.', 400)
        new_job_offer = JobOffer(
        
         title=data['title'],
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
        
        return new_job_offer

    def offresEmploi(self, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails):
        return jobOffer_repo.offresEmploi(needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
    
    def createJobOffer(self, data, employerId, isApproved, last_modified_by_id):
        new_job_offer = self.validateJobOffer(data, employerId, isApproved, last_modified_by_id)
        return jobOffer_repo.createJobOffer(new_job_offer)
    
    def offresEmploiEmployeur(self, employerId, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails):
        return jobOffer_repo.offresEmploiEmployeur(employerId, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
    
    def updateJobOffer(self, data):
        job_offer = self.validateJobOffer(data, data['employerId'], data['isApproved'], data['last_modified_by_id'])
        job_offer.id = data['id']
        return jobOffer_repo.updateJobOffer(job_offer)

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