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
            logger.warning("Login attempt failed on user: " + email + " user not found")
            raise LoginException()
        try:
            if user.active:
                if hasher.verify(user.password, password):
                    token = encode({'email': user.email, 'exp' : datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30),'active': user.active,'isModerator': user.isModerator,'firstName': user.firstName,'lastName': user.lastName}, os.environ.get('SECRET_KEY'))  
                    return token
            else:
                raise LoginException(True)
        except Exception as e:
            if hasattr(e, 'errorCode') and e.errorCode == 403:
                raise e
            else:
                logger.warning("Login attempt failed on user: " + email + " could not verify : ", e)
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
            logger.warning("Admin (" + current_user.email + ") tried to remove itself")

    def desactivateUser(self, current_user, userEmail):
        user = User.query.filter_by(email=userEmail).first()

        if user != current_user:
            auth_repo.updateActive(user, not user.active)
        else:
            logger.warning("Admin (" + current_user.email + ") tried to desactivate itself")

    
    def linkToExisting(self, offer, selectedEnterpriseId):
        employer = employer_repo.getEmployer(offer.employerId)

        if employer.enterpriseId == selectedEnterpriseId:
            # cas 1 : on utilise l'entreprise créée par l'utilisateur
            enterprise = enterprise_repo.getEnterprise(employer.enterpriseId)
            enterprise_repo.endEnterpriseTemporary(enterprise)
        else :
            # cas 2 : l'utilisateur a créé un doublon, on va le relier à l'entreprise existante.
            user = auth_repo.getUserById(employer.userId)
            duplicatedEnterprise = enterprise_repo.getEnterprise(employer.enterpriseId)
            if (not duplicatedEnterprise.isTemporary):
                enterprise_repo.deleteEnterprise(duplicatedEnterprise.id)
                employer_repo.linkEmployerEnterprise(user.id, selectedEnterpriseId)
            else:
                raise Exception("trying to delete a non temporary enterprise.")