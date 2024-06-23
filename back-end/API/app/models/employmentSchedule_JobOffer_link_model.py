from app import db

class EmploymentSchedule_JobOffer_link(db.Model):
    __tablename__ = 'employment_schedule__job_offer_link'
    id = db.Column(db.Integer, primary_key=True)
    jobOfferId = db.Column(db.Integer, db.ForeignKey('job_offer.id'), nullable=False)
    employmentScheduleId = db.Column(db.Integer, db.ForeignKey('employment_schedule.id'), nullable=False)



    def __repr__(self):
        return f"EmploymentSchedule_JobOffer_link(employmentScheduleId={self.employmentScheduleId}, jobOfferId={self.jobOfferId})"
    
    def to_json_string(self):
        return {
            "id": self.id,
            "JobOfferId": self.jobOfferId,
            "employmentScheduleId": self.employmentScheduleId
        }