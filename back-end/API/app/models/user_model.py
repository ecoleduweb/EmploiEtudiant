from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(300), default=False)
    active = db.Column(db.Boolean, default=False)
    isModerator = db.Column(db.Boolean, default=False)
    #Enventuellement, un employeur vérifié pourrait publier des offres d'emplois sans passer par le processus d'approbation.
    verified = db.Column(db.Boolean, nullable=False , default=False)
    # Relations
    enterpriseId = db.Column(db.Integer, db.ForeignKey("enterprise.id"), nullable=True)
    enterprise = db.relationship("Enterprise", back_populates="users")

    def __repr__(self):
        return f"User('{self.firstName}','{self.lastName}','{self.email}', '{self.password}', '{self.active}',  '{self.isModerator}', '{self.verified}', '{self.enterpriseId}')"