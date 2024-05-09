from app import db
from app.models.jobOffer_model import JobOffer
from app.models.employers_model import Employers
from app.models.enterprise_model import Enterprise
from app.models.user_model import User
from datetime import date
from flask import Flask, jsonify
from app.controllers.email_controller import sendMail

class JobOfferRepo:

    def createJobOffer(self, data, employerId, isApproved):
        new_job_offer = JobOffer(title=data['title'],
         description=data['description'],
         offerDebut=data["offerDebut"],
         address=data['address'],
         dateEntryOffice=data['dateEntryOffice'],
         deadlineApply=data['deadlineApply'],
         email=data['email'],
         hoursPerWeek=data['hoursPerWeek'],
         compliantEmployer=data['compliantEmployer'],
         internship=data['internship'],
         offerLink=data['offerLink'],
         salary=data['salary'],
         active=data['active'],
         employerId=employerId,
         scheduleId=data['scheduleId'],
         isApproved=isApproved)
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
        jobOffer.compliantEmployer = data['jobOffer']['compliantEmployer']
        jobOffer.internship = data['jobOffer']['internship']
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
    
    def approveJobOffer(self, data):
        jobOffer = JobOffer.query.filter_by(id=data['id']).first()
        jobOffer.isApproved = data['isApproved']
        jobOffer.approbationMessage = data['approbationMessage']
        user_id = Employers.query.filter_by(id=jobOffer.employerId).first().userId
        email = User.query.filter_by(id=user_id).first().email
        sendMail(email, "Approbation d'une offre d'emploi", "L'offre d'emploi avec le nom " + jobOffer.title + " a été approuvée!")
        db.session.commit()
        return jsonify({'message': 'job offer approved'})