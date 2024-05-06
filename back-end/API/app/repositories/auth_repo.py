from app import db
from app.models.user_model import User
from flask import Flask, jsonify, request
from argon2 import PasswordHasher
from jwt import encode
import datetime
import os
from logging import getLogger
logger = getLogger(__name__)

hasher = PasswordHasher()

class AuthRepo:

    def register(self, data):
        hashed_password = hasher.hash(data['password'])
        new_user = User(firstName=data['firstName'], lastName=data['lastName'], email=data['email'], password=hashed_password, active=True, isModerator = False)
        db.session.add(new_user)
        db.session.commit()
        try:
            token = encode({'email': data['email'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),'active': True,'isModerator': new_user.isModerator,'firstName': new_user.firstName,'lastName': new_user.lastName}, os.environ.get('SECRET_KEY'))
            logger.warn("Register successful on user: " + data['email'])      
            return jsonify({'token' : token})
        except Exception as e:
            logger.warn("Register failed on email: " + data['email'])
            return jsonify({'message': "could not verify"}), 401

    def updatePassword(self, data):
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return jsonify({'message': 'no user found'})
        user.password = hasher.hash(data['password'])
        db.session.commit()
        return jsonify({'message': 'password updated'})

    def getUser(self, email):
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return user
            else:
                return None
        except:
            return jsonify({'message': 'error occurred'})

    def getAllUsers(self):
        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['name'] = user.name
            user_data['email'] = user.email
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)
        return jsonify({'users': output})
