from app import db
from app.models.enterprise_model import Enterprise

class EnterpriseRepo:
    def createEnterprise(self, data, isTemporary):
        enterprise = Enterprise(name=data['name'], email=data['email'], phone=data['phone'], address=data['address'], cityId=data['cityId'], isTemporary=isTemporary)
        db.session.add(enterprise)
        db.session.commit()
        return enterprise
