from app import db
from app.models.enterprise_model import Enterprise
from app.models.employers_model import Employers
from flask import Flask, jsonify, request
from logging import getLogger
logger = getLogger(__name__)

class EnterpriseRepo:
    def getEnterprises(self):
        enterprises = Enterprise.query.all()
        return enterprises
    
    def createEnterprise(self, data, isTemporary):
        enterprise = Enterprise(name=data['name'], email=data['email'], phone=data['phone'], address=data['address'], cityId=data['cityId'], isTemporary=isTemporary)
        db.session.add(enterprise)
        db.session.commit()
        return enterprise
    
    def getEnterpriseByEmployer(self, employerId):
        employer = Employers.query.filter_by(id=employerId).first()
        if(employer == None):
            return None
        else: 
            enterprise = Enterprise.query.filter_by(id=employer.enterpriseId).first()
            return enterprise

    def getEnterprise(self, id):
        try:
            enterprise = Enterprise.query.filter_by(id=id).first()
            if enterprise:
                return enterprise
            else:
                return None
        except Exception as e:
            logger.error("Error : could not get enterprise" + str(e))
    
    def updateEnterprise(self, data):
        enterprise = Enterprise.query.filter_by(id=data['id']).first()
        enterprise.name = data['name']
        enterprise.email = data['email']
        enterprise.phone = data['phone']
        enterprise.address = data['address']
        enterprise.cityId = data['cityId']
        db.session.commit()
        logger.warn('enterprise updated')
        return enterprise
    
    def deleteEnterprise(self, id):
        enterprise = Enterprise.query.filter_by(id=id).first()
        if enterprise.isTemporary == True:
            db.session.delete(enterprise)
            db.session.commit()
        else:
           logger.error('enterprise is not temporary')
           return False
        logger.warning('enterprise deleted')
        return True
    def getEntrepriseId(self, name):
        enterprise = Enterprise.query.filter_by(name=name).first()
        return enterprise.id