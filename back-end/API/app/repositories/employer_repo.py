from app import db
from app.models.employers_model import Employers
from app.models.user_model import User
from flask import jsonify
from logging import getLogger
logger = getLogger(__name__)

class EmployerRepo:
    def createEmployer(self, enterpriseId, userId):
        # employer = Employers(data)
        employer = Employers(verified=False, userId=userId, enterpriseId=enterpriseId)
        db.session.add(employer)
        db.session.commit()
        return employer
    
    def getEmployer(self, id):
        employer = Employers.query.filter_by(id=id).first()
        return employer
    
    def linkEmployerEnterprise(self, userId, enterpriseId):
        employer = Employers.query.filter_by(userId=userId).first()
        employer.enterprise_id = enterpriseId
        db.session.commit()

    def updateEmployer(self, data, idEmployer):
        employer = Employers.query.filter_by(id=idEmployer).first()
        employer.verified = data['verified']
        db.session.commit()
        return employer
    
    def getEmployerByUserId(self, userId):
        employer = Employers.query.filter_by(userId=userId).first()
        return employer
            
    def removeUserIdFromEmployer(self, userId):
        employers = Employers.query.filter_by(userId=userId).all()
        for employer in employers:
                employer.userId = None
        db.session.commit()
