def verifyStringLen(string, expectedLen):
    length = len(string)
    if length > 0 and length <= expectedLen:
        return True
    else:
        raise Exception("String length invalid")