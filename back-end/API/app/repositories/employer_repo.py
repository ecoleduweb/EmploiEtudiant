from app import db
from app.models.employers_model import Employers
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
        employer = Employers.query.filter_by(userId=id).first()
        return employer
    
    def linkEmployerEnterprise(self, data):
        employer = Employers.query.filter_by(user_id=data['userId']).first()
        employer.enterprise_id = data['enterpriseId']
        db.session.commit()
        return jsonify({'message': 'employer linked to enterprise'})

    def getEmployerByEnterpriseId(self, enterpriseId):
        employer = Employers.query.filter_by(enterprise_id=enterpriseId).first()
        return employer

    def updateEmployer(self, data, idEmployer):
        employer = Employers.query.filter_by(id=idEmployer).first()
        employer.verified = data['verified']
        db.session.commit()
        return employer
    
    def deleteEmployer(self, id):
        employer = Employers.query.filter_by(id=id).first()
        if employer.verified == False:
            db.session.delete(employer)
            db.session.commit()
        else:
            logger.error('employer is verified')
            return False
        logger.warning('employer deleted')
        return True
    
    def getEmployerByUserId(self, userId):
        employer = Employers.query.filter_by(userId=userId).first()
        return employer
            

