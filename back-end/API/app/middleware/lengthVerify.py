from app.customexception.CustomException import ValidationException

def verifyStringLen(field, string, expectedLen):
    length = len(string)
    if length > 0 and length <= expectedLen:
        return True
    else:
        raise ValidationException(field, f"Ce champ doit comporter entre 1 et {expectedLen} caracteres.")