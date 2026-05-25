from app.repositories.enterprise_repo import EnterpriseRepo
from app.dtos.enterprise_dto import (
    EnterpriseCreateDTO,
    EnterpriseReadDTO,
    EnterpriseUpdateDTO
)
from app.customexception.exception import PermissionException

from logging import getLogger
logger = getLogger(__name__)
enterprise_repo = EnterpriseRepo()

class EnterpriseService:

    def get_all(self) -> list[EnterpriseReadDTO]:
        return enterprise_repo.get_all()
    
    def create(self, dto: EnterpriseCreateDTO, is_temporary: bool) -> EnterpriseReadDTO:
        dto.isTemporary = is_temporary
        return enterprise_repo.create(dto)
    
    def find_by_id(self, id) -> EnterpriseReadDTO:
        return enterprise_repo.find_by_id(id)
    
    def update(self, dto: EnterpriseUpdateDTO, current_user) -> EnterpriseReadDTO:
        if not current_user.isModerator:
            if current_user.enterpriseId != dto.id:
                logger.warning("An user tried to modify an entreprise don't have permission")
                raise PermissionException("Un utilisateur ne peut modifier que son entreprise")
            # Setting the isTemporary field to the current value in the database to prevent a user from changing it when updating their enterprise
            enterprise = enterprise_repo.find_by_id(current_user.enterpriseId)
            dto.IsTemporary = enterprise.isTemporary
        return enterprise_repo.update(dto)
    
    def delete_by_id(self, id) -> EnterpriseReadDTO:
        return enterprise_repo.delete_by_id(id)