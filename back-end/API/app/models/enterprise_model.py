from app import db

class Enterprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    isTemporary = db.Column(db.Boolean, nullable=False)
    # Relations
    cityId = db.Column(db.Integer, db.ForeignKey("city.id"), nullable=False)
    city = db.relationship("City", back_populates="enterprises")
    jobOffers = db.relationship("JobOffer", back_populates="enterprise")
    users = db.relationship("User", back_populates="enterprise")

    def __repr__(self):
        return f"Enterprise(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', address='{self.address}', cityId={self.cityId}, isTemporary={self.isTemporary})"
    