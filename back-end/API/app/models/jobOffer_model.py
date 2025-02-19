from app import db
from flask_sqlalchemy import SQLAlchemy

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
    active = db.Column(db.Boolean, nullable=False)
    approbationMessage = db.Column(db.String(6000))
    employerId = db.Column(db.Integer, nullable=True)
    isApproved = db.Column(db.Boolean, nullable=True, default=None)
    approvedDate = db.Column(db.DateTime, nullable=True, default=None) ## Date d'approbation de l'offre par l'administratrice
    last_modified_by_id = db.Column(db.Integer, nullable=True)

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
        active='{self.active}',
        approbationMessage='{self.approbationMessage}',
        employerId='{self.employerId}',
        isApproved='{self.isApproved}',
        approvedDate='{self.approvedDate}',
        last_modified_by_id='{self.last_modified_by_id}')'''

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
                'isApproved': self.isApproved,
                'approvedDate': self.approvedDate,
                'last_modified_by_id': self.last_modified_by_id
            }
        
    def to_json_string_without_approbation_message(self):
        result = self.to_json_string()

        del result['approbationMessage']
        return result