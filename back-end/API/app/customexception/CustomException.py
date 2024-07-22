class NotFoundException(Exception):
    def __init__(self, message="Ressource non trouvée"):
        super().__init__(message)
        self.message = message
        self.errorCode = 404

    def __str__(self):
        return f"(Error {str(self.errorCode)}) {self.message}"


class LoginException(Exception):
    def __init__(self, AccountDesactivated: bool = False, message="Impossible de se connecter"):
        errorCode = 401
        errorMessage = message + ": informations invalide"

        if AccountDesactivated:
            errorCode = 403
            errorMessage = message + ": compte désactiver"

        super().__init__(errorMessage)
        self.message = errorMessage
        self.errorCode = errorCode