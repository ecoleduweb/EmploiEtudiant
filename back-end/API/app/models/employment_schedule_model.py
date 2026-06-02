from app import db
from app.models.associations import job_offer_employment_schedule

class EmploymentSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    jobOffers = db.relationship(
        "JobOffer",
        secondary=job_offer_employment_schedule,
        back_populates="employmentSchedules",
    )

    def __repr__(self):
        return f"EmploymentSchedule(id={self.id}, description={self.description})"
    