import requests
import os
class CaptchaService:
    def verify_captcha(self, token):
        key = os.environ.get('RECAPTCHA_KEY')
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {
            "secret": key,
            "response": token
        }
        print("test")
        response = requests.post(url, data=params)
        result = response.json()
        if result['success'] and result['score'] >= 0.5:
            return True
        else:
            print("Captcha verification failed")
            return False