from app import db

class jobOffer(db.Model):
    
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
    urgent = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    EmployerId = db.Column(db.integer, nullable=False)
    ScheduleId = db.Column(db.integer, nullable=False)

    def __repr__(self):
        return f"jobOffer('{self.task}', '{self.title}')"