from app import db
from app.models.employmentSchedule_model import EmploymentSchedule
from flask import jsonify

class EmploymentScheduleRepo:
    def employmentSchedule(self, employmentScheduleId):
        employmentSchedule = EmploymentSchedule.query.filter_by(id=employmentScheduleId).first()
        print(employmentSchedule)
        return employmentSchedule
    
    def employmentSchedules(self):
        employmentSchedules = EmploymentSchedule.query.all()
        return employmentSchedules
    
    def employmentScheduleId(self, description):
        employmentSchedule = EmploymentSchedule.query.filter_by(description=description).first()
        print(employmentSchedule)
        employmentScheduleId = employmentSchedule.id
        return employmentScheduleId
