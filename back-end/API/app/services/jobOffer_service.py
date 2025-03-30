from app.repositories.jobOffer_repo import JobOfferRepo
from app.repositories.enterprise_repo import EnterpriseRepo
from app.repositories.study_program_repo import StudyProgramRepo
from app.models.jobOffer_model import JobOffer
from app.models.JobOffer_details import JobOfferDetails
from datetime import datetime
from app.middleware.lengthVerify import verifyStringLen
from app.middleware.numberVerify import verifyNumber
from app.customexception.CustomException import ValidationException, NotFoundException
from app.services.offer_program_service import OfferProgramService
from app.services.employmentSchedule_service import EmploymentScheduleService
from app.services.email_service import sendMail
import os
import re
offer_program_service = OfferProgramService()
employment_schedule_service = EmploymentScheduleService()
jobOffer_repo = JobOfferRepo()
enterprise_repo = EnterpriseRepo()
studyProgram_repo = StudyProgramRepo()
class JobOfferService:

    def validateJobOffer(self, data, employerId, isApproved, last_modified_by_id):
        verifyStringLen('title', data['title'], 255)
        verifyStringLen('address', data['address'], 255)
        verifyStringLen('email', data['email'], 255)
        if data['offerLink'] != "":
            verifyStringLen('offerLink', data['offerLink'], 255)
        verifyStringLen('salary', data['salary'], 255)
        verifyNumber('hoursPerWeek', data['hoursPerWeek'], [float, int])
        if not (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', data['email'])):
            raise ValidationException('email', 'Le format du courriel est invalide.')
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
         last_modified_by_id=last_modified_by_id)
        
        return new_job_offer
    
    def DidEmployerChangeTextOfJobOfferOrUpdateValueOfRejectedJobOffer(self, current_user, jobOffer, data):
        # Check if user is admin
        if current_user.isModerator:
            return False
        # Vérifier si le titre ou la description d'une offre a changé
        if jobOffer.title != data["title"] or jobOffer.description != data["description"]:
            return True
        
        if not jobOffer.isApproved and (jobOffer.title != data["title"] 
                                        or jobOffer.description != data["description"] 
                                        or jobOffer.offerDebut != data["offerDebut"] 
                                        or jobOffer.address != data["address"] 
                                        or jobOffer.dateEntryOffice != data["dateEntryOffice"] 
                                        or jobOffer.deadlineApply != data["deadlineApply"]
                                        or jobOffer.email != data["email"]
                                        or jobOffer.hoursPerWeek != data["hoursPerWeek"]
                                        or jobOffer.offerLink != data["offerLink"]
                                        or jobOffer.salary != data["salary"]
                                        or jobOffer.active != data["active"]
                                        ):
            return True

    def offresEmploi(self, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails):
        return jobOffer_repo.offresEmploi(needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
    
    def createJobOffer(self, data, employerId, isApproved, last_modified_by_id):
        new_job_offer = self.validateJobOffer(data, employerId, isApproved, last_modified_by_id)
        return jobOffer_repo.createJobOffer(new_job_offer)

    def deleteJobOffer(self, id):
        return jobOffer_repo.deleteJobOffer(id)
    
    def offresEmploiEmployeur(self, employerId, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails):
        return jobOffer_repo.offresEmploiEmployeur(employerId, needsEntrepriseDetails, needsEmploymentScheduleDetails, needsStudyProgramDetails)
    
    def updateJobOffer(self, data, current_user, id):
        jobOfferToUpdate = self.findById(id)
        if not jobOfferToUpdate:
            raise NotFoundException("Job offer not found.")
        
        data["jobOffer"]["employerId"] = jobOfferToUpdate.employerId
        data["jobOffer"]["isApproved"] = jobOfferToUpdate.isApproved
        if(self.DidEmployerChangeTextOfJobOfferOrUpdateValueOfRejectedJobOffer(current_user, jobOfferToUpdate, data["jobOffer"])):
            data["jobOffer"]["isApproved"] = None
            data["jobOffer"]["approbationMessage"] = None
        job_offer = self.validateJobOffer(data["jobOffer"], data["jobOffer"]["employerId"], data["jobOffer"]["isApproved"], current_user.id)
        job_offer.id = data["jobOffer"]["id"]
        employment_schedule_service.linkOfferSchedule(data["scheduleIds"], job_offer.id)
        # update offerProgram
        if 'studyPrograms' in data:
            offer_program_service.updateOfferProgram(job_offer.id, data['studyPrograms'])
        if job_offer.isApproved != data["jobOffer"]["isApproved"] and job_offer.isApproved == None:
            if not current_user.isModerator:
                sendMail(current_user.email, "Modification d'une offre d'emploi", "L'offre d'emploi au nom de <b>" + job_offer.title + "</b> a été modifiée avec succès. <br> Veuillez prévoir un délai moyen de 24 à 48 heures ouvrables pour la mise à jour de votre offre. <br> Vous recevrez un courriel lorsque votre offre modifiée sera affichée sur le Portail d'offres d'emploi du Cégep de Rivière-du-Loup. ")
            else:
                sendMail(os.environ.get('MAIL_ADMINISTRATOR_ADDRESS'), "Confirmation de modification d'une offre d'emploi", "L'offre d'emploi au nom de <b>" + job_offer.title + "</b> a été modifiée avec succès.")
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