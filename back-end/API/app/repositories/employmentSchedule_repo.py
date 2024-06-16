from app import db
from app.models.employmentSchedule_model import EmploymentSchedule
from app.models.jobOffer_model import JobOffer
from app.models.employmentSchedule_JobOffer_link_model import EmploymentSchedule_JobOffer_link
from flask import jsonify

class EmploymentScheduleRepo:
    def employmentSchedule(self, employmentScheduleId):
        employmentSchedule = EmploymentSchedule.query.filter_by(id=employmentScheduleId).first()
        return employmentSchedule
    
    def employmentSchedules(self):
        employmentSchedules = EmploymentSchedule.query.all()
        return employmentSchedules
    
    def employmentScheduleId(self, description):
        employmentSchedule = EmploymentSchedule.query.filter_by(description=description).first()
        employmentScheduleId = employmentSchedule.id
        return employmentScheduleId
    
    def removeExistingLinks(self, jobOfferId):
        EmploymentSchedule_JobOffer_link.query.filter_by(jobOfferId=jobOfferId).delete()
        db.session.commit()
    
    def linkOfferSchedule(self, scheduleIds, jobOfferId):
        self.removeExistingLinks(jobOfferId)
        for scheduleId in scheduleIds:
            link = EmploymentSchedule_JobOffer_link(jobOfferId=jobOfferId, employmentScheduleId=scheduleId)
            db.session.add(link)
        db.session.commit()

    def getScheduleFromJobOffer(self, jobOfferId):
        schedules = EmploymentSchedule.query.join(EmploymentSchedule_JobOffer_link, EmploymentSchedule_JobOffer_link.employmentScheduleId == EmploymentSchedule.id).filter(EmploymentSchedule_JobOffer_link.jobOfferId == jobOfferId).all()
        return schedules