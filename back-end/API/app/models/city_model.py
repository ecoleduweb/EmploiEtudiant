from app import db
from sqlalchemy.orm import relationship

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    idRegion = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False) 

    enterprises = relationship("Enterprise", back_populates="city")  

    def __repr__(self):
        return f"City('{self.id}', '{self.city}', '{self.idRegion}')"