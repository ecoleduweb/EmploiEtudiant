from logging import getLogger
from argon2 import PasswordHasher
import datetime
import os
from app.repositories.user_repo import UserRepo
from app.customexception.exception import PermissionException
from app.repositories.enterprise_repo import EnterpriseRepo
from app.utils.SanitizeDOM import sanitize_html
from app.dtos.user_dto import (
    UserLoginDTO,
    UserUpdateDTO,
    UserRegisterDTO,
    UserReadDTO,
    UserUpdatePasswordDTO
)
user_repo = UserRepo()
enterprise_repo = EnterpriseRepo()
logger = getLogger(__name__)

hasher = PasswordHasher()


class UserService:
    def get_all(self) -> list[UserReadDTO]:
        return user_repo.get_all()

    def find_by_id(self, id) -> UserReadDTO:
        return user_repo.find_by_id(id)
    
    def find_by_email(self, email) -> UserReadDTO:
        return user_repo.find_by_email(email)
    
    def update_reset_password(self, email, new_password):
        user = user_repo.find_by_email(email)
        user.password = hasher.hash(new_password)
        user_repo.update(user)

    def update_password(self, current_user, dto: UserUpdatePasswordDTO) -> UserReadDTO:
        if not current_user.isModerator and current_user.id != dto.id:
            raise PermissionException(f"L'utilisateur {current_user.id} n'a pas la permission de modifier le mot de passe de l'utilisateur {user.id}")
        user = user_repo.find_by_id(dto.id)
        user.password = hasher.hash(dto.password)
        user = user_repo.update(user)
        return user
    
    def update_name_and_email(self, current_user, dto: UserUpdateDTO) -> UserReadDTO:
        user = user_repo.find_by_id(dto.id)
        if not current_user.isModerator and  current_user.id != user.id:
            raise PermissionException(f"L'utilisateur {current_user.id} n'a pas la permission de modifier les informations de l'utilisateur {user.id}")
        
        user.email = dto.email
        user.firstName = sanitize_html(dto.firstName)
        user.lastName = sanitize_html(dto.lastName)

        return user_repo.update(user)

    def toggle_admin(self, current_user, id) -> UserReadDTO:
        user = user_repo.find_by_id(id)
        if current_user.id == user.id:
            raise PermissionException("Un administrateur ne peut pas changer son propre statut d'administrateur")
        user.isModerator = not user.isModerator
        return user_repo.update(user)

    def delete(self, current_user, id: int) -> UserReadDTO:
        user = user_repo.find_by_id(id)

        if user.id == current_user.id:
            raise PermissionException("Un utilisateur ne peut pas se supprimer lui même")
        return user_repo.delete(user)

    def toggle_active(self, current_user, id: int) -> UserReadDTO:
        user = user_repo.find_by_id(id)
        if user.id == current_user.id:
            raise PermissionException("Un administrateur ne peut pas se désactiver lui même")
        user.active = not user.active
        user_repo.update(user)
        return user
    
    def manage_temporary_enterprise(self, selected_enterprise_id, previous_enterprise_id) -> UserReadDTO:
        previous_enterprise = enterprise_repo.find_by_id(previous_enterprise_id)
        selected_enterprise = enterprise_repo.find_by_id(selected_enterprise_id)
        # si l'entreprise n'est pas temporaire, on ne fait rien
        print(previous_enterprise_id, selected_enterprise_id, previous_enterprise.isTemporary, selected_enterprise.isTemporary)
        # L'entreprise perd sont status de temporaire.
        if previous_enterprise_id == selected_enterprise_id and selected_enterprise.isTemporary:
            enterprise_repo.end_enterprise_temporary(previous_enterprise)
        # On lie l'employeur à l'entreprise ciblée et on supprime l'entreprise temporaire
        elif previous_enterprise.isTemporary:
            user_repo.update_users_enterprise_id(previous_enterprise_id, selected_enterprise_id)
            enterprise_repo.delete_by_id(previous_enterprise_id)