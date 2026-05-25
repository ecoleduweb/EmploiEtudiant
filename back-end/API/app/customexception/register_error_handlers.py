# app/error_handlers.py
import logging
from flask import Flask
from app.customexception.exception import DuplicateException, NotFoundException, ValidationException, PermissionException, LoginException
from pydantic import ValidationError

FR_MESSAGES = {
    # Core types
    "int_parsing": "la valeur n'est pas un entier valide",
    "float_parsing": "la valeur n'est pas une valeur flottante valide",
    "bool_parsing": "la valeur n'est pas un booléen valide",
    "decimal_parsing": "la valeur n'est pas une valeur décimale valide",
    "str_type": "type str attendu",
    "bytes_type": "type d'octet attendu",
    "list_type": "la valeur n'est pas une liste valide",
    "dict_type": "la valeur n'est pas un dict valide",
    "enum": "la valeur n'est pas un membre valide de l'énumération ; autorisé : {expected}",

    # Required & Extra
    "missing": "champ obligatoire",
    "extra_forbidden": "champs supplémentaires non autorisés",

    # Numbers  (pydantic v2 ctx keys: gt / ge / lt / le / multiple_of)
    "greater_than":        "s'assurer que cette valeur est supérieure à {gt}",
    "greater_than_equal":  "s'assurer que cette valeur est supérieure ou égale à {ge}",
    "less_than":           "s'assurer que cette valeur est inférieure à {lt}",
    "less_than_equal":     "s'assurer que cette valeur est inférieure ou égale à {le}",
    "multiple_of":         "s'assurer que cette valeur est un multiple de {multiple_of}",
    "finite_number":       "s'assurer que cette valeur est un nombre fini",

    # String / Items length  (ctx keys: min_length / max_length / pattern)
    "string_too_short":         "s'assurer que cette valeur comporte au moins {min_length} caractères",
    "string_too_long":          "s'assurer que cette valeur comporte au maximum {max_length} caractères",
    "too_short":                "s'assurer que cette valeur contient au moins {min_length} éléments",
    "too_long":                 "s'assurer que cette valeur contient au maximum {max_length} éléments",
    "string_pattern_mismatch":  "la chaîne ne correspond pas à regex \"{pattern}\"",

    # Date/Time
    "date_future": "la date n'est pas dans le futur",
    "date_past": "la date n'est pas dans le passé",
    "date_parsing": "format de date non valide",
    "datetime_parsing": "format de date/heure non valide",
    "time_parsing": "format d'heure non valide",

    # Network / Specialized
    "value_error":  "la valeur n'est pas valide",     # pydantic v2 catch-all (incl. EmailStr)
    "url_parsing":  "URL non valide",
    "url_scheme":   "schéma d'URL non valide ou manquant",
    "uuid_parsing": "la valeur n'est pas un uuid valide",
}

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
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        raw_errors = e.errors(include_url=False, include_input=False)

        formatted_errors = []
        for err in raw_errors:
            err_type = err["type"]
            ctx = err.get("ctx") or {}
            msg_template = FR_MESSAGES.get(err_type, err["msg"])

            try:
                message = msg_template.format(**ctx)
            except (KeyError, IndexError):
                # ctx didn't provide a placeholder we expected — fall back to pydantic's msg
                message = err["msg"]

            formatted_errors.append({
                "field": ".".join(str(p) for p in err["loc"]),
                "message": message,
                "type": err_type,
            })

        logger.info("Validation error: %s", formatted_errors)
        return formatted_errors, 400

    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        # le filet de sécurité : tout ce qui n'a pas été attrapé ci-dessus
        logger.exception("Unhandled exception", exc_info=e)
        return {"error": "Internal server error"}, 500