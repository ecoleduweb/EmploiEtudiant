# app/error_handlers.py
import logging
from flask import Flask
from app.customexception.exception import DuplicateException, NotFoundException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(NotFoundException)
    def handle_not_found(e: NotFoundException):
        logger.warning("Resource not found: %s", e.message)
        return {'message': e.message}, e.errorCode


    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        # le filet de sécurité : tout ce qui n'a pas été attrapé ci-dessus
        logger.exception("Unhandled exception", exc_info=e)
        return {"error": "Internal server error"}, 500