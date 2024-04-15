from app import db
from app.models.jobOffer_model import JobOffer
from flask import Flask, jsonify

class JobOfferRepo:

    def createJobOffer(self, data, employerId):
        new_job_offer = JobOffer(title=data['title'], description=data['description'], address=data['address'], dateEntryOffice=data['dateEntryOffice'], deadlineApply=data['deadlineApply'], email=data['email'], hoursPerWeek=data['hoursPerWeek'], compliantEmployer=data['compliantEmployer'], internship=data['internship'], offerStatus=data['offerStatus'], offerLink=data['offerLink'], salary=data['salary'], urgent=data['urgent'], active=data['active'], employerId=employerId, scheduleId=data['scheduleId'])
        db.session.add(new_job_offer)
        db.session.commit()
        return new_job_offer

    def offreEmploi(self, id):
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