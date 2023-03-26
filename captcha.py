import logging
import os
import time

from twocaptcha import TwoCaptcha

url = "https://online.mfa.gov.ua/application"
sitekey = "6LcPNjgbAAAAAIp0KyR2RK_e7gb6ECDXR0n-JLqG"
captcha_api_key = os.getenv("2CAPTCHA_API_KEY")

solver = TwoCaptcha(captcha_api_key)


def solve_captcha():
    logging.info("Trying to solve captcha")
    s_time = time.time()
    try:
        result = solver.recaptcha(sitekey=sitekey, url=url)
    except Exception as e:
        raise Exception(f"Failed to solve captcha {str(e)}")
    logging.info(f"Captcha solved in {time.time() - s_time :.2f} sec")
    return result.get('code')
