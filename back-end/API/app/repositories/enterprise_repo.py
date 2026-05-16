from app import db
from app.models.enterprise_model import Enterprise
from app.models.employers_model import Employers
from app.models.user_model import User
from logging import getLogger

logger = getLogger(__name__)


class EnterpriseRepo:

    def endEnterpriseTemporary(self, enterprise):
        try:
            enterprise = Enterprise.query.filter_by(id=enterprise.id).first()
            if not enterprise:
                return None

            enterprise.isTemporary = False
            db.session.commit()
            return enterprise

        except Exception as e:
            db.session.rollback()
            logger.warning("Error : could not get enterprise " + str(e))
            return None

    def getEnterprises(self):
        enterprises = Enterprise.query.all()
        for enterprise in enterprises:
            enterprise.users = User.query.join(
                Employers, Employers.userId == User.id
            ).filter(
                Employers.enterpriseId == enterprise.id
            ).all()
        return enterprises

    def getAllEmployersFromEntreprise(self, id):
        return Employers.query.filter_by(enterpriseId=id).all()

    def createEnterprise(self, enterprise: Enterprise, isTemporary: bool):
        try:
            enterprise.isTemporary = isTemporary
            db.session.add(enterprise)
            db.session.flush()

            for uid in enterprise.userIds:
                employer = Employers.query.filter_by(userId=uid).first()

                if employer:
                    employer.enterpriseId = enterprise.id
                else:
                    logger.warning("user not found")

            db.session.commit()
            return enterprise

        except Exception as e:
            db.session.rollback()
            raise e

    def getEnterpriseByEmployer(self, employerId):
        employer = Employers.query.filter_by(userId=employerId).first()
        if not employer:
            return None

        return Enterprise.query.filter_by(id=employer.enterpriseId).first()

    def getEmployerFromEntreprise(self, id):
        employer = Employers.query.filter_by(enterpriseId=id).first()
        return employer if employer else None

    def getEnterprise(self, id):
        try:
            enterprise = Enterprise.query.filter_by(id=id).first()

            if enterprise:
                enterprise.users = User.query.join(
                    Employers, Employers.userId == User.id
                ).filter(
                    Employers.enterpriseId == id
                ).all()

            return enterprise

        except Exception as e:
            logger.error("Error : could not get enterprise " + str(e))
            return None

    def updateEnterprise(self, enterprise: Enterprise):
        try:
            enterprise_entity = Enterprise.query.get(enterprise.id)
            if not enterprise_entity:
                return None
            print(enterprise.userIds)
            print(enterprise)
            enterprise_entity.name = enterprise.name
            enterprise_entity.email = enterprise.email
            enterprise_entity.phone = enterprise.phone
            enterprise_entity.address = enterprise.address
            enterprise_entity.cityId = enterprise.cityId

      
            #on fera pas un update mais un delete  parce que la base donnée n'est pas configuré pour faire un update dans ce cas là
            if enterprise.userIds:
                for uid in enterprise.userIds:
                    employer = Employers.query.filter_by(userId=uid).first()

                    if employer:
                        employer.enterpriseId = enterprise_entity.id
                    else:
                        db.session.add(
                            Employers(
                                userId=uid,
                                enterpriseId=enterprise_entity.id,
                                verified=False
                            )
                        )

            db.session.commit()
            return enterprise_entity

        except Exception as e:
            db.session.rollback()
            raise e

    def deleteEnterprise(self, id):
        enterprise = Enterprise.query.filter_by(id=id).first()

        if not enterprise:
            return False

        if enterprise.isTemporary:
            db.session.delete(enterprise)
            db.session.commit()
            return True

        logger.error("enterprise is not temporary")
        return False

    def getEnterpriseId(self, name):
        enterprise = Enterprise.query.filter_by(name=name).first()
        return enterprise.id if enterprise else None

    def getEnterpriseByEmployerId(self, employerId):
        employer = Employers.query.filter_by(id=employerId).first()

        if not employer:
            return None

        return Enterprise.query.filter_by(id=employer.enterpriseId).first()