from logging import getLogger
from flask import current_app
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import datetime
from jwt import encode
import os
from app.repositories.user_repo import UserRepo
from app.services.captcha_service import CaptchaService
from app.customexception.exception import LoginException, NotFoundException, RecaptchaException, DuplicateException
from app.utils.SanitizeDOM import sanitize_html
from app.dtos.user_dto import (
    UserRegisterDTO,
    UserLoginDTO,
)
user_repo = UserRepo()
captcha_service = CaptchaService()
logger = getLogger(__name__)

hasher = PasswordHasher()
# TODO quand on met le mauvais mot de passe, ca dit compte desactive
class AuthService:
    def login(self, dto: UserLoginDTO):
        try:
            user = user_repo.find_by_email(dto.email)
            if not user.active:
                raise LoginException(True, f"Impossible de se connecter avec l'email: {dto.email}")
            hasher.verify(user.password, dto.password)
            return self._generateToken(user), user
        except VerifyMismatchError:
            raise LoginException(f"Login attempt failed on user: {dto.email} invalid password")
        except NotFoundException:
            logger.warning(f"Login attempt failed on user: {dto.email} user not found")
            raise LoginException()
        except LoginException as e:
            raise e
        except Exception as e:
            logger.error(f"Login attempt failed on user: {dto.email} unexpected error", exc_info=e)
            raise LoginException()

    def register(self, dto: UserRegisterDTO):
        if not current_app.config.get('TESTING'):
            if not captcha_service.verify_captcha(dto.captchaToken):
                raise RecaptchaException()
        
        try :
            user_repo.find_by_email(dto.email)
            # should raise NotFoundException if the user is not found, which is what we want in this case
            logger.warning(f"Registration attempt failed on user: {dto.email} email already exists")
            raise DuplicateException("Le courriel existe déjà")
        except NotFoundException:
            # should raise NotFoundException if the user is not found, which is what we want in this case
            pass
        dto.firstName = sanitize_html(dto.firstName)
        dto.lastName = sanitize_html(dto.lastName)  
        dto.password = hasher.hash(dto.password)
        dto.enterpriseId = None
        dto.enterprise = None
        dto.isModerator = False
        dto.verified = False
        dto.active = True

        new_user = user_repo.create(dto)
        token = self._generateToken(new_user)
        return token, new_user

    def _generateToken(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),
            'active': user.active,
            'isModerator': user.isModerator,
            'firstName': user.firstName,
            'lastName': user.lastName
        }
        return encode(payload, os.environ.get('SECRET_KEY'))