from app import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    idRegion = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.city}', '{self.idRegion}')"