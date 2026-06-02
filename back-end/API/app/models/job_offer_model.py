from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from app.models.associations import (
    job_offer_study_program,
    job_offer_employment_schedule
)

class JobOffer(db.Model):

    __tablename__ = 'job_offer'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(100000), nullable=False)
    offerDebut = db.Column(db.Date, nullable=False) ## Date de publication de l'offre. L'offre est affichée à partir de cette date.
    dateEntryOffice = db.Column(db.Date, nullable=False) ## Date d'entrée en fonction de l'emploi
    deadlineApply = db.Column(db.Date, nullable=False) ## Date limite pour postuler. L'offre est retirée à cette date.
    email = db.Column(db.String(255), nullable=False)
    hoursPerWeek = db.Column(db.Float, nullable=False)
    offerLink = db.Column(db.String(255))
    salary = db.Column(db.String(255), nullable=False)
    approbationMessage = db.Column(db.String(6000))
    isApproved = db.Column(db.Boolean, nullable=True, default=None)
    approvedDate = db.Column(db.DateTime, nullable=True, default=None) ## Date d'approbation de l'offre par l'administratrice
    last_modified_by_id = db.Column(db.Integer, nullable=True)
    lastModifiedDate  = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) ## Date de la dernière modification de l'offre

    #Relations    
    enterpriseId = db.Column(db.Integer, db.ForeignKey("enterprise.id"), nullable=False)
    enterprise = db.relationship("Enterprise", back_populates="jobOffers")
    studyPrograms = db.relationship(
        "StudyProgram",
        secondary=job_offer_study_program,
        back_populates="jobOffers",
    )
    employmentSchedules = db.relationship(
        "EmploymentSchedule",
        secondary=job_offer_employment_schedule,
        back_populates="jobOffers",
    )



    def __repr__(self):
        return f'''JobOffer(id={self.id},
        title='{self.title}',
        address='{self.address}',
        description='{self.description}',
        offerDebut='{self.offerDebut}' , 
        dateEntryOffice='{self.dateEntryOffice}',
        deadlineApply='{self.deadlineApply}',
        email='{self.email}',
        hoursPerWeek={self.hoursPerWeek},
        offerLink='{self.offerLink}',
        salary='{self.salary}',
        approbationMessage='{self.approbationMessage}',
        enterpriseId='{self.enterpriseId}',
        isApproved='{self.isApproved}',
        approvedDate='{self.approvedDate}',
        lastModifiedDate='{self.lastModifiedDate}',
        last_modified_by_id='{self.last_modified_by_id}')'''