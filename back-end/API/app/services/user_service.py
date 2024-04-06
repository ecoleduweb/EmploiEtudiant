from flask import jsonify
from argon2 import PasswordHasher
import datetime
from jwt import encode
import os
from app.repositories.auth_repo import AuthRepo
auth_repo = AuthRepo()

hasher = PasswordHasher()

class UserService:
    def login(self, email, password):
        user = auth_repo.getUser(email)

        if user is None:
            return jsonify({'message': 'user not found'}), 401
        try:
            isvalid = hasher.verify(user.password, password)

            token = encode({'email': user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),'active': user.active,'isModerator': user.isModerator}, os.environ.get('SECRET_KEY'))
            return jsonify({'token' : token})
        except Exception as e:
            return jsonify({'message': "could not verify"}), 401

    
    def createUser(self, data):
        return auth_repo.createUser(data)

    def getAllUsers(self):
        return auth_repo.getAllUsers()
    
    def getUser(self, email):
        return auth_repo.getUser(email)
    
    def updatePassword(self, data):
        return auth_repo.updatePassword(data)