from app import db
from app.models.jobOffer_model import JobOffer
from flask import Flask, jsonify

class JobOfferRepo:

    def createJobOffer(self, data, employerId):
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
         offerStatus=data['offerStatus'],
         offerLink=data['offerLink'],
         salary=data['salary'],
         active=data['active'],
         employerId=employerId,
         scheduleId=data['scheduleId'])
        db.session.add(new_job_offer)
        db.session.commit()
        return new_job_offer
    
    def offresEmploiEmployeur(self, employerId):
        jobOffers = JobOffer.query.filter_by(employerId=employerId).all()
        return jobOffers
    
    def updateJobOffer(self, data):
        jobOffer = JobOffer.query.filter_by(id=data['id']).first()
        jobOffer.title = data['title']
        jobOffer.description = data['description']
        jobOffer.address = data['address']
        jobOffer.offerDebut = data['offerDebut']
        jobOffer.dateEntryOffice = data['dateEntryOffice']
        jobOffer.deadlineApply = data['deadlineApply']
        jobOffer.email = data['email']
        jobOffer.hoursPerWeek = data['hoursPerWeek']
        jobOffer.compliantEmployer = data['compliantEmployer']
        jobOffer.internship = data['internship']
        jobOffer.offerStatus = data['offerStatus']
        jobOffer.offerLink = data['offerLink']
        jobOffer.salary = data['salary']
        jobOffer.active = data['active']
        jobOffer.employerId = data['employerId']
        jobOffer.scheduleId = data['scheduleId']
        db.session.commit()
        return jobOffer

    def offreEmploi(self,id):
        jobOffer = JobOffer.query.filter_by(id=id).first()
        return jobOffer

    def offresEmploi(self):
        jobOffers = JobOffer.query.all()
        return jobOffers
    
    def linkJobOfferEmployer(self, data):
        jobOffer = JobOffer.query.filter_by(id=data['jobOfferId']).first()
        jobOffer.employer_id = data['employerId']
        db.session.commit()
        return jsonify({'message': 'job offer linked to employer'})