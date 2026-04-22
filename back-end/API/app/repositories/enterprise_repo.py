from app import locale
from app import db
from app.models.enterprise_model import Enterprise
from app.models.employers_model import Employers
from app.customexception.CustomException import NotFoundException
from logging import getLogger
from app.models.user_model import User
logger = getLogger(__name__)

class EnterpriseRepo:
    def endEnterpriseTemporary(self, enterprise):
        try:
            enterprise = Enterprise.query.filter_by(id=enterprise.id).first()
            enterprise.isTemporary = False
            db.session.commit()
        except Exception as e:
            logger.warning("Error : could not get enterprise" + str(e))
            raise NotFoundException("Enterprise not found")
            
    def getEnterprises(self):
        enterprises = Enterprise.query.all()
        result = []
        
        for e in enterprises:
            users_obj = User.query \
                .join(Employers, Employers.userId == User.id) \
                .filter(Employers.enterpriseId == e.id) \
                .all()
            
            e_data = e.to_json_string() 
            
            e_data['users'] = [u.to_json_string() for u in users_obj]
            
            result.append(e_data)
            
        enterprises_sorted = sorted(result, key=lambda x: locale.strxfrm(x['name']))
        
        return enterprises_sorted   
    
    def createEnterprise(self, data, isTemporary): 
        try:
            enterprise = Enterprise(
                name=data.get('name'), 
                email=data.get('email'), 
                phone=data.get('phone'), 
                address=data.get('address'), 
                cityId=data.get('cityId'), 
                isTemporary=isTemporary
            )
            db.session.add(enterprise)
            db.session.flush() 

            users_list = data.get('users', [])
            if isinstance(users_list, list):
                for u in users_list:
                    u_id = u.get('id') if isinstance(u, dict) else u
                    if u_id:
                        employer = Employers.query.filter_by(userId=u_id).first()
                        
                        if employer:
                            employer.enterpriseId = enterprise.id
                        else:
                            employer = Employers(
                                userId=u_id, 
                                enterpriseId=enterprise.id, 
                                verified=False
                            )
                            db.session.add(employer)
            db.session.commit()
            return enterprise 
        except Exception as e:
            db.session.rollback()
            raise e
        

    def getEnterpriseByEmployer(self, employerId):
        employer = Employers.query.filter_by(id=employerId).first()
        if employer is None:
            return None
        enterprise = Enterprise.query.filter_by(id=employer.enterpriseId).first()
        return enterprise

    def getEmployerFromEntreprise(self, id):
        employer = Employers.query.filter_by(entrepriseId=id).first()
        if(employer == None):
            return None
        else:
            return employer

    def getEnterprise(self, id):
        try:
            enterprise = Enterprise.query.filter_by(id=id).first()
            if enterprise:
                enterprise.users = User.query \
                    .join(Employers, Employers.userId == User.id) \
                    .filter(Employers.enterpriseId == id) \
                    .all()
            return enterprise
        except Exception as e:
            logger.error("Error : could not get enterprise" + str(e))
            return None
    
    def updateEnterprise(self, data):
        try:
            enterprise = Enterprise.query.get(data['id'])
            if not enterprise:
                return None

            enterprise.name = data.get('name')
            enterprise.email = data.get('email')
            enterprise.phone = data.get('phone')
            enterprise.address = data.get('address')
            enterprise.cityId = data.get('cityId')

            users_list = data.get('users')
            if isinstance(users_list, list):
                self.updateUserEnterprise(enterprise.id, users_list)

            db.session.commit()
            return enterprise
            
        except Exception as e:
            db.session.rollback()
            raise e

    def updateUserEnterprise(self, enterprise_id, users_list):
        try:
            Employers.query.filter_by(enterpriseId=enterprise_id).delete()
            
            for u in users_list:
                u_id = u.get('id') if isinstance(u, dict) else u
                if u_id:
                    new_employer = Employers(
                        userId=u_id, 
                        enterpriseId=enterprise_id, 
                        verified=False
                    )
                    db.session.add(new_employer)
            db.session.flush()
        except Exception as e:
            raise e
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
    
    def getEnterpriseId(self, name):
        enterprise = Enterprise.query.filter_by(name=name).first()
        return enterprise.id
    
    def getEnterpriseByEmployerId(self, employerId):
        employer = Employers.query \
            .join(Enterprise, Employers.enterpriseId == Enterprise.id) \
            .filter(Employers.id == employerId) \
            .first()
        print("************************************************************************")
        print(employer)
        print("************************************************************************")

        return employer.enterprise
