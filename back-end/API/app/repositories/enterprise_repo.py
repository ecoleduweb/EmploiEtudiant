from turtle import update

from app import locale
from app import db
from app.models.enterprise_model import Enterprise
from app.models.user_model import User
from app.customexception.exception import NotFoundException
from app.dtos.enterprise_dto import (
    EnterpriseCreateDTO,
    EnterpriseUpdateDTO,
    EnterpriseReadDTO
)

from logging import getLogger
logger = getLogger(__name__)

class EnterpriseRepo:
    def end_enterprise_temporary(self, dto: EnterpriseReadDTO):
        enterprise = Enterprise.query.filter_by(id=dto.id).options(db.joinedload(Enterprise.users)).first()
        if enterprise is None:
            raise NotFoundException("Enterprise not found", dto.id)
        enterprise.isTemporary = False
        db.session.commit()
            
    def get_all(self) -> list[EnterpriseReadDTO]:
        enterprises = Enterprise.query.options(db.joinedload(Enterprise.users)).all()
        enterprises_sorted = sorted(enterprises, key=lambda e: locale.strxfrm(e.name))
        dtos = [EnterpriseReadDTO.model_validate(e) for e in enterprises_sorted]
        return dtos
    
    def create(self, dto: EnterpriseCreateDTO) -> EnterpriseReadDTO:
        enterprise = Enterprise(**dto.model_dump())
        db.session.add(enterprise)
        db.session.commit()
        return EnterpriseReadDTO.model_validate(enterprise)

    def find_by_id(self, id) -> EnterpriseReadDTO:
        enterprise = Enterprise.query.filter_by(id=id).first()
        if enterprise is None:
            raise NotFoundException(f"Enterprise not found", id)
        return EnterpriseReadDTO.model_validate(enterprise)

    def find_by_user_id(self, user_id) -> EnterpriseReadDTO:
        enterprise = db.session.execute(
            db.select(Enterprise)
            .join(Enterprise.users)
            .where(User.id == user_id)
        ).scalar_one_or_none()
        if enterprise is None:
            raise NotFoundException(f"Enterprise not found with user id", user_id)
        return EnterpriseReadDTO.model_validate(enterprise)

    def update(self, dto: EnterpriseUpdateDTO) -> EnterpriseReadDTO:
        enterprise = Enterprise.query.filter_by(id=dto.id).options(db.joinedload(Enterprise.users)).first()
        if enterprise is None:
            raise NotFoundException("Enterprise not found", dto.id)
        enterprise.name = dto.name
        enterprise.email = dto.email
        enterprise.phone = dto.phone
        enterprise.address = dto.address
        enterprise.cityId = dto.cityId
        enterprise.isTemporary = dto.isTemporary
        for user in enterprise.users:
            # Cherche tous les utilisateurs qui avaient l'entrerprise avant la mise à jour
            # Mais qui n'en font plus parti.
            if user.id not in [u.id for u in dto.users]:
                User.query.filter_by(id=user.id).update({"enterpriseId": None})
        # Cherche tous les utilisateurs qui possèdent l'entreprise avec la mise à jour.
        for user in dto.users:
            if user.id not in [u.id for u in enterprise.users]:
                User.query.filter_by(id=user.id).update({"enterpriseId": enterprise.id})

        db.session.commit()
        return EnterpriseReadDTO.model_validate(enterprise)
    
    def delete_by_id(self, id):
        enterprise = Enterprise.query.filter_by(id=id).first()
        if enterprise is None:
            raise NotFoundException(f"Enterprise not found", id)
        db.session.delete(enterprise)
        db.session.commit()