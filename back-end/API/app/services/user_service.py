from logging import getLogger
from app.models.user_model import User
from app import db
from flask import jsonify, current_app
from argon2 import PasswordHasher
import datetime
from jwt import encode
import os
from app.repositories.auth_repo import AuthRepo
from app.repositories.employer_repo import EmployerRepo
from app.services.captcha_service import CaptchaService
auth_repo = AuthRepo()
captcha_service = CaptchaService()
employer_repo = EmployerRepo()
logger = getLogger(__name__)

hasher = PasswordHasher()


class UserService:
    def login(self, email, password):
        user = auth_repo.getUser(email)
        if user is None:
            logger.warn("Login attempt failed on user: " + email + " user not found")
            return jsonify({'message': 'user not found'}), 401
        try:
            if user.active:
                if hasher.verify(user.password, password):
                    token = encode({'email': user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),'active': user.active,'isModerator': user.isModerator,'firstName': user.firstName,'lastName': user.lastName}, os.environ.get('SECRET_KEY'))  
                    return jsonify({'token' : token})
            else:
                return jsonify({'AccountDesactivated': True}), 200
        except Exception as e:
            logger.warn("Login attempt failed on user: " + email + " could not verify : ", e)
            return jsonify({'message': "could not verify"}), 401

    def register(self, data):
        if not current_app.config.get('TESTING'):
            if not captcha_service.verify_captcha(data['captchaToken']):
                return jsonify({'message': 'Captcha verification failed'}), 400
        return auth_repo.register(data)

    def getAllUsers(self):
        return auth_repo.getAllUsers()

    def getUser(self, email):
        return auth_repo.getUser(email)

    def updatePassword(self, current_user, data):
        email = ""
        
        if current_user.isModerator:
            email = data["email"]
        else:
            email = current_user.email

        try:
            auth_repo.updatePassword(email, data["password"])
        except Exception as e:
            raise Exception("Failed to update password")
    
    def updateUser(self, current_user, data):
        email = ""

        if current_user.isModerator:
            email = data["email"]
        else:
            email = current_user.email
        
        try:
            auth_repo.updateUser(email, data)
        except Exception as e:
            raise Exception("Failed to update user")
        
    def makeAdmin(self, user):
        auth_repo.updateAdmin(user, not user.isModerator)
        db.session.commit()

    def removeUser(self, current_user, userEmail):
        user = User.query.filter_by(email=userEmail).first()

        if user != current_user:
            employer_repo.removeUserIdFromEmployer(user.id)
            auth_repo.removeUser(userEmail)

    def desactivateUser(self, current_user, userEmail):
        user = User.query.filter_by(email=userEmail).first()

        if user != current_user:
            auth_repo.updateActive(user, not user.active)