from app import db
from app.models.associations import job_offer_study_program

class StudyProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    jobOffers = db.relationship(
        "JobOffer",
        secondary=job_offer_study_program,
        back_populates="studyPrograms",
    )

    def __repr__(self):
        return f"Program('{self.id}', '{self.name}')"