from app import db
from sqlalchemy.orm import relationship
from app.models.employers_model import Employers

class JobOffer(db.Model):
    __tablename__ = 'job_offer'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False) 
    offerDebut = db.Column(db.Date, nullable=False)
    dateEntryOffice = db.Column(db.Date, nullable=False)
    deadlineApply = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    hoursPerWeek = db.Column(db.Float, nullable=False)
    offerLink = db.Column(db.String(255))
    salary = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    approbationMessage = db.Column(db.String, nullable=True) 
    employerId = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)
    isApproved = db.Column(db.Boolean, nullable=True, default=None)
    approvedDate = db.Column(db.DateTime, nullable=True, default=None)

    employer = relationship("Employers", back_populates="jobOffers")
    employmentSchedules = relationship("EmploymentSchedule", secondary="employment_schedule__job_offer_link", back_populates="jobOffers")

    def __repr__(self):
        return f'''JobOffer(id={self.id},
        title='{self.title}',
        address='{self.address}',
        description='{self.description}',
        offerDebut='{self.offerDebut}',
        dateEntryOffice='{self.dateEntryOffice}',
        deadlineApply='{self.deadlineApply}',
        email='{self.email}',
        hoursPerWeek={self.hoursPerWeek},
        offerLink='{self.offerLink}',
        salary='{self.salary}',
        active='{self.active}',
        approbationMessage='{self.approbationMessage}',
        employerId='{self.employerId}',
        isApproved='{self.isApproved}',
        approvedDate='{self.approvedDate}')'''

    def to_json_string(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'description': self.description,
            'offerDebut': str(self.offerDebut),
            'dateEntryOffice': str(self.dateEntryOffice),
            'deadlineApply': str(self.deadlineApply),
            'email': self.email,
            'hoursPerWeek': self.hoursPerWeek,
            'offerLink': self.offerLink,
            'salary': self.salary,
            'active': self.active,
            'approbationMessage': self.approbationMessage,
            'employerId': self.employerId,
            'isApproved': self.isApproved,
            'approvedDate': self.approvedDate
        }
    
    def to_dict(self, include_employer, include_employmentSchedules, include_studyPrograms):
        data = {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'description': self.description,
            'offerDebut': str(self.offerDebut),
            'dateEntryOffice': str(self.dateEntryOffice),
            'deadlineApply': str(self.deadlineApply),
            'email': self.email,
            'hoursPerWeek': self.hoursPerWeek,
            'offerLink': self.offerLink,
            'salary': self.salary,
            'active': self.active,
            'approbationMessage': self.approbationMessage,
            'employerId': self.employerId,
            'isApproved': self.isApproved,
            'approvedDate': self.approvedDate
        }
        if include_employer and include_employer.lower() != "false":
            data['employer'] = self.employer.to_dict() if self.employer else None
        if include_employmentSchedules != None and include_employmentSchedules != "false" :
            data['employmentSchedules'] = [schedule.to_dict() for schedule in self.employmentSchedules]
        if include_studyPrograms != None and include_studyPrograms != "false":
            data['studyPrograms'] = [program.to_dict() for program in self.studyPrograms]
        return data
