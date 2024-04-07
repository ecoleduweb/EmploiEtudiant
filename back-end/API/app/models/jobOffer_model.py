from app import db
from flask_sqlalchemy import SQLAlchemy

class JobOffer(db.Model):

    __tablename__ = 'job_offer'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    dateEntryOffice = db.Column(db.Date, nullable=False)
    deadlineApply = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    hoursPerWeek = db.Column(db.Float, nullable=False)
    compliantEmployer = db.Column(db.Boolean, nullable=False)
    internship = db.Column(db.Boolean, nullable=False)
    offerStatus = db.Column(db.Integer, nullable=False)
    offerLink = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    urgent = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    employerId = db.Column(db.Integer, nullable=True)
    scheduleId = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"JobOffer(id={self.id}, title='{self.title}', address='{self.address}', description='{self.description}', dateEntryOffice='{self.dateEntryOffice}', deadlineApply='{self.deadlineApply}', email='{self.email}', hoursPerWeek={self.hoursPerWeek}, compliantEmployer={self.compliantEmployer}, internship={self.internship}, offerStatus={self.offerStatus}, offerLink='{self.offerLink}', salary='{self.salary}', urgent={self.urgent}, active={self.active}, employerId={self.employerId}, scheduleId={self.scheduleId})"

    def to_json_string(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'description': self.description,
            'dateEntryOffice': str(self.dateEntryOffice),  # Convert datetime to string
            'deadlineApply': str(self.deadlineApply),  # Convert date to string
            'email': self.email,
            'hoursPerWeek': self.hoursPerWeek,
            'compliantEmployer': self.compliantEmployer,
            'internship': self.internship,
            'offerStatus': self.offerStatus,
            'offerLink': self.offerLink,
            'salary': self.salary,
            'urgent': self.urgent,
            'active': self.active,
            'employerId': self.employerId,
            'scheduleId': self.scheduleId
        }