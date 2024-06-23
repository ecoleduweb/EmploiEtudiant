from app import db

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Region('{self.id}', '{self.region}')"