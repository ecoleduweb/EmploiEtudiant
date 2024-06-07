class NotFoundException(Exception):
    def __init__(self, message="Ressource non trouvée"):
        super().__init__(message)
        self.message = message
        self.errorCode = 404

    def __str__(self):
        return f"(Error {str(self.errorCode)}) {self.message}"


