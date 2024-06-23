from app import db
from sqlalchemy.orm import relationship

class Enterprise(db.Model):
    __tablename__ = 'enterprise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    cityId = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    isTemporary = db.Column(db.Boolean, nullable=False)

    employers = relationship("Employers", back_populates="enterprise")
    city = relationship("City", back_populates="enterprises")

    def __repr__(self):
        return f"Enterprise(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}', address='{self.address}', cityId={self.cityId}, isTemporary={self.isTemporary})"
    
    def to_json_string(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'cityId': self.cityId,
            'isTemporary': self.isTemporary
        }