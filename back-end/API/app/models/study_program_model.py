from app import db
from sqlalchemy.orm import relationship

class StudyProgram(db.Model):
    __tablename__ = 'study_program'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    jobOffers = relationship("JobOffer", secondary="offer_program", primaryjoin="StudyProgram.id==OfferProgram.programId", 
                             secondaryjoin="JobOffer.id==OfferProgram.offerId", backref="studyPrograms")


    def __repr__(self):
        return f"Program('{self.id}', '{self.name}')"
    
    def to_json_string(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }