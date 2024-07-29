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
from app.customexception.CustomException import LoginException
from app.repositories.enterprise_repo import EnterpriseRepo
auth_repo = AuthRepo()
captcha_service = CaptchaService()
employer_repo = EmployerRepo()
enterprise_repo = EnterpriseRepo()
logger = getLogger(__name__)

hasher = PasswordHasher()


class UserService:
    def login(self, email, password):
        user = auth_repo.getUser(email)
        if user is None:
            logger.warn("Login attempt failed on user: " + email + " user not found")
            raise LoginException()
        try:
            if user.active:
                if hasher.verify(user.password, password):
                    token = encode({'email': user.email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30),'active': user.active,'isModerator': user.isModerator,'firstName': user.firstName,'lastName': user.lastName}, os.environ.get('SECRET_KEY'))  
                    return token
            else:
                raise LoginException(True)
        except Exception as e:
            if hasattr(e, 'errorCode') and e.errorCode == 403:
                raise e
            else:
                logger.warn("Login attempt failed on user: " + email + " could not verify : ", e)
                raise LoginException()

    def register(self, data):
        if not current_app.config.get('TESTING'):
            if not captcha_service.verify_captcha(data['captchaToken']):
                return jsonify({'message': 'Captcha verification failed'}), 400
        return auth_repo.register(data)

    def getAllUsers(self):
        return auth_repo.getAllUsers()

    def getUser(self, email):
        return auth_repo.getUser(email)
    
    def getUserById(self, id):
        return auth_repo.getUserById(id)

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
        else:
            logger.warn("Admin (" + current_user.email + ") tried to remove itself")

    def desactivateUser(self, current_user, userEmail):
        user = User.query.filter_by(email=userEmail).first()

        if user != current_user:
            auth_repo.updateActive(user, not user.active)
        else:
            logger.warn("Admin (" + current_user.email + ") tried to desactivate itself")

    
    def linkToExisting(offer, employer, user, enterprise, selectedEnterprise):
        if (offer != None and employer != None and user != None and enterprise != None and selectedEnterprise != None):
            if (enterprise.isTemporary and not selectedEnterprise.isTemporary):
                employer_repo.linkEmployerEnterprise(user.id, enterprise.id)
                enterprise_repo.deleteEnterprise(enterprise.id)
            else:
                raise Exception("Invalid")
        else:
            raise Exception("Invalid")