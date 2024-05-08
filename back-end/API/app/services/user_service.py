from logging import getLogger
from app.models.user_model import User
from app import db
from flask import jsonify
from argon2 import PasswordHasher
import datetime
from jwt import encode
import os
from app.repositories.auth_repo import AuthRepo
from app.services.captcha_service import CaptchaService
auth_repo = AuthRepo()
captcha_service = CaptchaService()
logger = getLogger(__name__)

hasher = PasswordHasher()


class UserService:
    def login(self, email, password):
        user = auth_repo.getUser(email)

        if user is None:
            return jsonify({'message': 'user not found'}), 401
        try:
            isvalid = hasher.verify(user.password, password)
            token = encode({'email': user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),'active': user.active,'isModerator': user.isModerator,'firstName': user.firstName,'lastName': user.lastName}, os.environ.get('SECRET_KEY'))
            logger.warn("Login attempt successful on user: " + email)      
            return jsonify({'token' : token})
        except Exception as e:
            logger.warn("Login attempt failed on user: " + email)
            return jsonify({'message': "could not verify"}), 401

    def register(self, data):
        print(data)
        if ((os.environ.get('ENVIRONMENT') is None) or (os.environ.get('ENVIRONMENT') == 'prod')):
            if not captcha_service.verify_captcha(data['captchaToken']):
                return jsonify({'message': 'Captcha verification failed'}), 400
        return auth_repo.register(data)

    def getAllUsers(self):
        return auth_repo.getAllUsers()

    def getUser(self, email):
        return auth_repo.getUser(email)

    def updatePassword(self, data):
        return auth_repo.updatePassword(data)
    
