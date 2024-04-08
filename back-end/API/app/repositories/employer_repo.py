from app import db
from app.models.employers_model import Employers
from flask import jsonify

class EmployerRepo:
    def createEmployer(self, enterpriseId, userId):
        # employer = Employers(data)
        employer = Employers(verified=False, userId=userId, enterpriseId=enterpriseId)
        db.session.add(employer)
        db.session.commit()
        return employer
    
    def linkEmployerEnterprise(self, data):
        employer = Employers.query.filter_by(user_id=data['userId']).first()
        employer.enterprise_id = data['enterpriseId']
        db.session.commit()
        return jsonify({'message': 'employer linked to enterprise'})
