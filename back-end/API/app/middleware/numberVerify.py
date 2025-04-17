from app.customexception.CustomException import ValidationException

def verifyNumber(field, data, formats):
    for format in formats:
        try:
            if isinstance(format(data), format):
                return True
        except ValueError:    
            raise ValidationException(field, "Ce champ doit correspondre a un nombre.")