# app/error_handlers.py
import logging
from flask import Flask
from app.customexception.exception import DuplicateException, NotFoundException, ValidationException, PermissionException, LoginException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(NotFoundException)
    def handle_not_found(e: NotFoundException):
        logger.warning(f"{e.message} for id : {e.id}", exc_info=e)
        return {'message': e.message}, e.errorCode

    @app.errorhandler(DuplicateException)
    def handle_duplicate(e: DuplicateException):
        logger.warning(f"{e.message} for field : {e.field}", exc_info=e)
        return {'message': e.message, 'field': e.field}, e.errorCode
    
    @app.errorhandler(ValidationException)
    def handle_validation(e: ValidationException):
        logger.warning(f"{e.message} for field : {e.field}", exc_info=e)
        return {'message': e.message, 'field': e.field}, e.errorCode
        
    @app.errorhandler(PermissionException)
    def handle_permission(e: PermissionException):
        logger.warning(e.message, exc_info=e)
        return {'message': e.message}, e.errorCode
            
    @app.errorhandler(LoginException)
    def handle_login(e: LoginException):
        logger.warning(e.message, exc_info=e)
        return {'message': e.message}, e.errorCode

    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        # le filet de sécurité : tout ce qui n'a pas été attrapé ci-dessus
        logger.exception("Unhandled exception", exc_info=e)
        return {"error": "Internal server error"}, 500