class NotFoundException(Exception):
    def __init__(self, message, id):
        super().__init__(message)
        self.message = message
        self.errorCode = 404
        self.id = id

    def __str__(self):
        return f"(Error {str(self.errorCode)}) {self.message}"


class LoginException(Exception):
    def __init__(self, AccountDesactivated: bool = False, message="Impossible de se connecter"):
        errorCode = 401
        errorMessage = message + ": informations invalide"

        if AccountDesactivated:
            errorCode = 403
            errorMessage = message + ": compte désactivé"
        print(errorMessage, errorCode)
        super().__init__(errorMessage)
        self.message = errorMessage
        self.errorCode = errorCode

class ValidationException(Exception):
    def __init__(self, field, message):
        super().__init__(field, message)
        self.errorCode = 400
        self.field = field
        self.message = message

class DuplicateException(Exception):
    def __init__(self, field, message):
        super().__init__(field, message)
        self.errorCode = 400
        self.field = field
        self.message = message

class RecaptchaException(Exception):
    def __init__(self, message="Captcha verification failed"):
        super().__init__(message)
        self.message = message
        self.errorCode = 400

class PermissionException(Exception):
    def __init__(self, message="Vous n'avez pas la permission d'effectuer cette action"):
        super().__init__(message)
        self.message = message
        self.errorCode = 403
