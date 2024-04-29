from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(300), default=False)
    active = db.Column(db.Boolean, default=False)
    isModerator = db.Column(db.Boolean, default=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), default=False)

    def __repr__(self):
        return f"User('{self.firstName}','{self.lastName}','{self.email}', '{self.password}', '{self.active}',  '{self.isModerator}')"
    
    def to_json_string(self):
        return {'id': self.id, 'firstName':self.firstName, 'lastName':self.lastName, 'email': self.email, 'password': self.password, "active": self.active, 'isModerator': self.isModerator}
