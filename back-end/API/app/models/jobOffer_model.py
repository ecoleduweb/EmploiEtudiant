from app import db
from flask_sqlalchemy import SQLAlchemy

class JobOffer(db.Model):

    __tablename__ = 'job_offer'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(30000), nullable=False)
    offerDebut = db.Column(db.Date, nullable=False)
    dateEntryOffice = db.Column(db.Date, nullable=False)
    deadlineApply = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    hoursPerWeek = db.Column(db.Float, nullable=False)
    offerLink = db.Column(db.String(255))
    salary = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    approbationMessage = db.Column(db.String(6000))
    employerId = db.Column(db.Integer, nullable=True)
    scheduleId = db.Column(db.Integer, nullable=True)
    isApproved = db.Column(db.Boolean, nullable=True, default=None)

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
        active={self.active},
        approbationMessage='{self.approbationMessage}',
        employerId={self.employerId},
        scheduleId={self.scheduleId}),
        isApproved={self.isApproved}'''

    def to_json_string(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'description': self.description,
            'offerDebut': str(self.offerDebut),
            'dateEntryOffice': str(self.dateEntryOffice),  # Convert datetime to string
            'deadlineApply': str(self.deadlineApply),  # Convert date to string
            'email': self.email,
            'hoursPerWeek': self.hoursPerWeek,
            'offerLink': self.offerLink,
            'salary': self.salary,
            'active': self.active,
            'approbationMessage': self.approbationMessage,
            'employerId': self.employerId,
            'scheduleId': self.scheduleId,
            'isApproved': self.isApproved
        }