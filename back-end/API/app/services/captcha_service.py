import requests
import os
from logging import getLogger
logger = getLogger(__name__)

class CaptchaService:
    def verify_captcha(self, token):
        key = os.environ.get('RECAPTCHA_KEY')
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            "secret": key,
            "response": token
        }
        response = requests.post(url, data=params)
        result = response.json()
        if result['success'] and result['score'] >= 0.5:
            logger.warn("Captcha verification successful")
            return True
        else:
            logger.warn("Captcha verification failed")
            return False