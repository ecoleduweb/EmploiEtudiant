from app import db
from sqlalchemy.orm import relationship

class EmploymentSchedule(db.Model):
    __tablename__ = 'employment_schedule'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)

    jobOffers = relationship("JobOffer", secondary="employment_schedule__job_offer_link", back_populates="employmentSchedules")

    def __repr__(self):
        return f"EmploymentSchedule(id={self.id}, description={self.description})"
    
    def to_json_string(self):
        return {
            "id": self.id,
            "description": self.description
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description

        }