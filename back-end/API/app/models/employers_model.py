from app import db
from sqlalchemy.orm import relationship

class Employers(db.Model):
    __tablename__ = 'employers'

    id = db.Column(db.Integer, primary_key=True)
    verified = db.Column(db.Boolean, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    enterpriseId = db.Column(db.Integer, db.ForeignKey('enterprise.id'), nullable=False)

    jobOffers = relationship("JobOffer", back_populates="employer")
    enterprise = relationship("Enterprise", back_populates="employers")
    user = relationship("User", back_populates="employers")

    def __repr__(self):
        return f"Employers(id={self.id}, verified={self.verified}, userId={self.userId}, enterpriseId={self.enterpriseId})"

    def to_json_string(self):
        return {
            'id': self.id,
            'verified': self.verified,
            'userId': self.userId,
            'enterpriseId': self.enterpriseId
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'verified': self.verified,
            'userId': self.userId,
            'enterpriseId': self.enterpriseId
        }