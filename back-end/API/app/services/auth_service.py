import json
from logging import getLogger
from flask import current_app
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timezone, timedelta
from jwt import encode
from app.utils.Encryption import encrypt
import os
from app.repositories.user_repo import UserRepo
from app.services.captcha_service import CaptchaService
from app.customexception.exception import LoginException, NotFoundException, RecaptchaException, DuplicateException, ValidationException
from app.utils.SanitizeDOM import sanitize_html
from app.services.email_service import send_mail
from app.services.user_service import UserService
from app.dtos.user_dto import (
    UpdatedUserReadDTO,
    UserRegisterDTO,
    UserLoginDTO,
)
user_repo = UserRepo()
captcha_service = CaptchaService()
logger = getLogger(__name__)
user_service = UserService()
hasher = PasswordHasher()

# TODO quand on met le mauvais mot de passe, ca dit compte desactive
# Reset password, la route n'existe plus :(
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
    
    def request_reset_password(self, email):
        try:
            user = user_repo.find_by_email(email)
            userData = {
                "email": user.email,
                "resetDate": str(datetime.now().timestamp())
            }
            passwordResetToken = encrypt(json.dumps(userData))
            passwordResetLink = ( str.encode(os.environ.get("URL")) + b"/resetPassword?token=" + passwordResetToken).decode("utf-8")
            logger.info(passwordResetLink)
            if not send_mail(user.email, 'Demande de changement de mot de passe', 'Vous avez demandé un changement de mot de passe.<br> Si vous n\'avez pas fait cette requête, veuillez ignorer ce courriel.<br><b><a href="https://' + passwordResetLink + '" target="_blank">Réinitialiser votre mot de passe.</a></b>'):
                raise LoginException("Failed to send reset password email")
        except NotFoundException:
            logger.warning("A user tried to reset but provided a bad email")
            raise LoginException(False, "Le courriel fourni pour la réinitialisation est invalide (Aucun utilisateur trouvé/invalide)")

    #TODO valider si le champ de confirmation de mot de passe valide que les deux champs sont identiques et validésa avec Felt
    def reset_password(self, email, new_passord, reset_date) -> UpdatedUserReadDTO:
        if (reset_date + 900) <= datetime.now().timestamp():
            raise LoginException(True, "Le lien de réinitialisation a expiré, veuillez faire une nouvelle demande de réinitialisation de mot de passe")

        return user_service.reset_password(email, new_passord)
    
    def _generateToken(self, user):
        payload = {
            'id': user.id,
            'email': user.email,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=30),
            'active': user.active,
            'isModerator': user.isModerator,
            'firstName': user.firstName,
            'lastName': user.lastName
        }
        return encode(payload, os.environ.get('SECRET_KEY'))