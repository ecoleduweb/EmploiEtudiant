from app import locale
from app import db
from app.models.user_model import User
from logging import getLogger
from app.dtos.user_dto import (
    UserLoginResponseDTO,
    UserUpdateDTO,
    UserRegisterDTO,
    UserReadDTO
)
from app.customexception.exception import NotFoundException
logger = getLogger(__name__)


class UserRepo:
    def create(self, dto: UserRegisterDTO) -> UserReadDTO:
        new_user = User(**dto.model_dump(exclude={"captchaToken"}, exclude_unset=True))
        db.session.add(new_user)
        db.session.commit()
        return UserReadDTO.model_validate(new_user)

    def update(self, dto: UserUpdateDTO) -> UserReadDTO:
        user = User.query.filter_by(id=dto.id).first()
        if not user:
            raise NotFoundException("user not found", dto.id)
        user.verified = dto.verified
        user.enterpriseId = dto.enterpriseId
        user.isModerator = dto.isModerator
        user.active = dto.active
        user.email = dto.email
        user.firstName = dto.firstName
        user.lastName = dto.lastName
        if dto.password != None or dto.password != "":
            user.password = dto.password
        db.session.commit()
        return UserReadDTO.model_validate(user)
    
    def delete(self, dto: UserReadDTO):
        User.query.filter_by(id=dto.id).delete()
        db.session.commit()

    def find_by_email(self, email: str) -> UserLoginResponseDTO:
        user = User.query.filter_by(email=email).first()
        if user is None:
            raise NotFoundException("user not found", email)
        return UserLoginResponseDTO.model_validate(user)

    def find_by_id(self, id) -> UserReadDTO:
        user = User.query.filter_by(id=id).first()
        if user is None:
            raise NotFoundException("user not found", id)
        return UserReadDTO.model_validate(user)
    
    def update_users_enterprise_id(self, original_enterprise_id, new_enterprise_id) -> list[UserReadDTO]:
        users = User.query.filter_by(enterpriseId=original_enterprise_id).all()
        for user in users:
            user.enterpriseId = new_enterprise_id
        db.session.commit()
        return [UserReadDTO.model_validate(user) for user in users]

    def get_all(self) -> list[UserReadDTO]:
        users = User.query.options(db.joinedload(User.enterprise)).all()
        users_sorted = sorted(users, key=lambda e: locale.strxfrm(e.name))
        dtos = [UserReadDTO.model_validate(e) for e in users_sorted]
        return dtos
