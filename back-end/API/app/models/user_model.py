from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), default=False)
    active = db.Column(db.Boolean, default=False)
    isModerator = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.email}', '{self.password}', '{self.active}',  '{self.isModerator}')"
    
    def to_json_string(self):
        return {'id': self.id, 'email': self.email, 'password': self.password, "active": self.active, 'isModerator': self.isModerator}