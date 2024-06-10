from app import db
from app.models.jobOffer_model import JobOffer
from app.models.employers_model import Employers
from app.models.enterprise_model import Enterprise
from app.models.user_model import User
from datetime import date
from flask import Flask, jsonify
from operator import attrgetter

class JobOfferRepo:

    def createJobOffer(self, data, employerId, isApproved, approvedDate=None):
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
         scheduleId=data['scheduleId'],
         isApproved=isApproved,
         approvedDate=approvedDate)
        db.session.add(new_job_offer)
        db.session.commit()
        return new_job_offer
    
    def offresEmploiEmployeur(self, employerId):
        jobOffers = JobOffer.query.filter_by(employerId=employerId).all()
        return jobOffers
    
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
        jobOffer.scheduleId = data['jobOffer']['scheduleId']

        if 'isApproved' in data['jobOffer']:
            jobOffer.isApproved = data['jobOffer']['isApproved']
            
        if 'approbationMessage' in data['jobOffer']:
            jobOffer.approbationMessage = data['jobOffer']['approbationMessage'] 
        db.session.commit()
        return jobOffer

    def offreEmploi(self,id):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        return jobOffer

    def offresEmploi(self):
        jobOffers = JobOffer.query.all()
        return jobOffers
    
    def offresEmploiApproved(self):
        today = date.today()
        jobOffers = JobOffer.query.filter(
            JobOffer.isApproved == True,
            JobOffer.offerDebut <= today,
            JobOffer.deadlineApply >= today
        ).all()
        return jobOffers
    
    def linkJobOfferEmployer(self, data):
        jobOffer = JobOffer.query.filter_by(id=data['jobOfferId']).first()
        jobOffer.employer_id = data['employerId']
        db.session.commit()
        return jsonify({'message': 'job offer linked to employer'})
    
    def approveJobOffer(self, id, isApproved, approbationMessage):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        jobOffer.isApproved = isApproved
        jobOffer.approbationMessage = approbationMessage
        db.session.commit()

    def updateApprovedDate(self, id):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        jobOffer.approvedDate = date.today()
        db.session.commit()

    def resetApprovedDate(self, id):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        jobOffer.approvedDate = None
        db.session.commit()

    def getMostRecents(self):
        today = date.today()
        
        jobOffers = JobOffer.query.filter(
            JobOffer.isApproved == True,
            JobOffer.offerDebut <= today,
            JobOffer.deadlineApply >= today
        ).all()

        jobOffersOrdred = sorted(jobOffers, key=attrgetter("approvedDate"), reverse=True)[:5] #J'ai beaucoup de problèmes avec celle-ci (devras voir)

        return jobOffersOrdred