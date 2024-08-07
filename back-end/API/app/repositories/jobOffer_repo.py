from app import db
from app.models.jobOffer_model import JobOffer
from app.models.employers_model import Employers
from app.models.enterprise_model import Enterprise
from app.models.JobOffer_details import JobOfferDetails
from app.models.employmentSchedule_JobOffer_link_model import EmploymentSchedule_JobOffer_link
from app.models.employmentSchedule_model import EmploymentSchedule
from app.models.study_program_model import StudyProgram
from app.models.offer_programm_model import OfferProgram
from app.models.user_model import User
from datetime import date, timedelta, datetime
from flask import Flask, jsonify
from operator import attrgetter

class JobOfferRepo:

    def createJobOffer(self, newJobOffer):
        db.session.add(newJobOffer)
        db.session.commit()
        return newJobOffer
    
    def offresEmploiEmployeur(self, employerId, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails):
        jobOffers = JobOffer.query.filter_by(employerId=employerId).all()
        return self.addDetailsToJobOffer(jobOffers, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
    
    def updateJobOffer(self, data):
        jobOffer = JobOffer.query.filter_by(id=data['jobOffer']['id']).first()
        jobOffer.title = data['jobOffer']['title']
        jobOffer.description = data['jobOffer']['description']
        jobOffer.address = data['jobOffer']['address']
        jobOffer.offerDebut = data['jobOffer']['offerDebut']
        jobOffer.dateEntryOffice = data['jobOffer']['dateEntryOffice']
        jobOffer.deadlineApply = data['jobOffer']['deadlineApply']
        jobOffer.email = data['jobOffer']['email']
        jobOffer.hoursPerWeek = data['jobOffer']['hoursPerWeek']
        jobOffer.offerLink = data['jobOffer']['offerLink']
        jobOffer.salary = data['jobOffer']['salary']
        jobOffer.active = data['jobOffer']['active']
        jobOffer.employerId = data['jobOffer']['employerId']

        if 'isApproved' in data['jobOffer']:
            jobOffer.isApproved = data['jobOffer']['isApproved']
            
        if 'approbationMessage' in data['jobOffer']:
            jobOffer.approbationMessage = data['jobOffer']['approbationMessage'] 
        db.session.commit()
        return jobOffer

    def offreEmploi(self,id):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        return jobOffer

    def offresEmploi(self, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails):
        jobOffers = JobOffer.query.all()
        return self.addDetailsToJobOffer(jobOffers, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
    
    def getOffers(self, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails):
        today = date.today()
        jobOffers = JobOffer.query.filter(
            JobOffer.isApproved == True,
            JobOffer.offerDebut <= today,
            JobOffer.deadlineApply >= today
        ).order_by(JobOffer.approvedDate.desc()).all()
        return self.addDetailsToJobOffer(jobOffers, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
    
    def getRecentOffers(self, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails):
        today = date.today()
        last_week = today - timedelta(days=7)
        jobOffers = JobOffer.query.filter(
            JobOffer.isApproved == True,
            JobOffer.offerDebut <= today,
            JobOffer.deadlineApply >= today,
            JobOffer.approvedDate > last_week
        ) \
        .order_by(JobOffer.approvedDate.desc()).all()

        # If no recents job offers are found, then we get the latest 5.
        if len(jobOffers) == 0:
            jobOffers = JobOffer.query.filter(
                JobOffer.isApproved == True,
                JobOffer.offerDebut <= today,
                JobOffer.deadlineApply >= today
            )\
            .order_by(JobOffer.approvedDate.desc()) \
            .limit(5) \
            .all()

        jobOffers = self.addDetailsToJobOffer(jobOffers, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails)
        return jobOffers
    
    def addDetailsToJobOffer(self, jobOffers, getEntrepriseDetails, employmentScheduleDetails, studyProgramDetails): 
        jobOffersDetails = []
        for jobOffer in jobOffers:
            jobOfferDetails = JobOfferDetails(jobOffer)
            if getEntrepriseDetails:
                enterprise = Enterprise.query \
                    .join(Employers, Employers.enterpriseId == Enterprise.id) \
                    .filter(Employers.id == jobOffer.employerId) \
                    .first()
                jobOfferDetails.AddEnterprise(enterprise)
            if employmentScheduleDetails:
                schedules = EmploymentSchedule.query \
                    .join(EmploymentSchedule_JobOffer_link, EmploymentSchedule_JobOffer_link.employmentScheduleId == EmploymentSchedule.id) \
                    .filter(EmploymentSchedule_JobOffer_link.jobOfferId == jobOffer.id) \
                    .all()
                jobOfferDetails.AddSchedules(schedules)
            if studyProgramDetails:
                studyPrograms = StudyProgram.query \
                    .join(OfferProgram, OfferProgram.programId == StudyProgram.id) \
                    .filter(OfferProgram.offerId == jobOffer.id) \
                    .all()
                jobOfferDetails.AddStudyPrograms(studyPrograms)
            jobOffersDetails.append(jobOfferDetails)
        return jobOffersDetails

    def linkJobOfferEmployer(self, data):
        jobOffer = JobOffer.query.filter_by(id=data['jobOfferId']).first()
        jobOffer.employer_id = data['employerId']
        db.session.commit()
        return jsonify({'message': 'job offer linked to employer'})
    
    def approveJobOffer(self, id, isApproved, approbationMessage):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        jobOffer.isApproved = isApproved
        jobOffer.approbationMessage = approbationMessage
        if jobOffer.isApproved:
            jobOffer.approvedDate = datetime.now()
        db.session.commit()

    def archiveJobOffer(self, id):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        jobOffer.deadlineApply = date.today() - timedelta(days=1)
        db.session.commit()

    def jobOfferExist(self, id):
        return JobOffer.query.filter_by(id=id).first() is not None