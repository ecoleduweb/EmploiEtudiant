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
            return jsonify({'token' : token})
        except Exception as e:
            logger.warn("Register failed on email: " + data['email'] + " could not verify : " + str(e))
            return jsonify({'message': "could not verify"}), 401

    def updatePassword(self, email, password):
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.warn("Couldn't update password for user with email: " + email + " user not found")
            return jsonify({'message': 'no user found'})
        
        user.password = hasher.hash(password)
        db.session.commit()

    def updateUser(self, email, data):
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.warn("Couldn't update user with email: " + email + ", user not found")
            return jsonify({'message': 'no user found'})
            
        if type(data["lastname"]) == str and data["lastname"] != " ":
            user.lastName = data["lastname"]
            
        if type(data["firstname"]) == str and data["firstname"] != " ":
            user.firstName = data["firstname"]

        db.session.commit()

    def getUser(self, email):
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return user
            else:
                logger.warn("Couldn't get user with email: " + email + " user not found")
                return None
        except:
            return jsonify({'message': 'error occurred'})

    def getAllUsers(self):
        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['firstName'] = user.firstName
            user_data['lastName'] = user.lastName
            user_data['email'] = user.email
            user_data['password'] = user.password
            user_data['active'] = user.active
            user_data['isModerator'] = user.isModerator
            output.append(user_data)
        return jsonify({'users': output})
