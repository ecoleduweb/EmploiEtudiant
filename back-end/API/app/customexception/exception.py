class NotFoundException(Exception):
    def __init__(self, message, id):
        super().__init__(message)
        self.message = message
        self.error_code = 404
        self.id = id

    def __str__(self):
        return f"(Error {str(self.error_code)}) {self.message}"


class LoginException(Exception):
    def __init__(self, message="Impossible de se connecter", account_desactivated: bool = False):
        error_code = 401
        error_message = message + ": informations invalide"
        if account_desactivated:
            error_code = 403
            error_message = message + ": compte désactivé"
        super().__init__(error_message)
        self.message = error_message
        self.error_code = error_code

class ValidationException(Exception):
    def __init__(self, field, message):
        super().__init__(field, message)
        self.error_code = 400
        self.field = field
        self.message = message

class DuplicateException(Exception):
    def __init__(self, field, message):
        super().__init__(field, message)
        self.error_code = 400
        self.field = field
        self.message = message

class RecaptchaException(Exception):
    def __init__(self, message="Captcha verification failed"):
        super().__init__(message)
        self.message = message
        self.error_code = 400

class PermissionException(Exception):
    def __init__(self, message="Vous n'avez pas la permission d'effectuer cette action"):
        super().__init__(message)
        self.message = message
        self.error_code = 403
