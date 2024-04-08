from app import db

class OfferProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    programId = db.Column(db.Integer, nullable=False)
    offerId = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"OfferProgram('{self.id}', '{self.programId}', '{self.offerId}')"
    
    def to_json_string(self):
        return {
            "id": self.id,
            "programId": self.programId,
            "offerId": self.offerId
        }