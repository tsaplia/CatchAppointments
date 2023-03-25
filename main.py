import logging
import os
import time
from datetime import date

import requests
from twocaptcha import TwoCaptcha

from config import consulate_id, country_id, service_id, delay,  sound_name
from flare_solverr import FSSession

sound_path = f"{os.getcwd()}\\{sound_name}"

url = "https://online.mfa.gov.ua/application"
session_url = "https://online.mfa.gov.ua/api/v1/auth/session"

sitekey = "6LcPNjgbAAAAAIp0KyR2RK_e7gb6ECDXR0n-JLqG"
captcha_api_key = os.getenv("2CAPTCHA_API_KEY")

today = date.today().strftime("%Y-%m-%d")
appointment_url = f"https://online.mfa.gov.ua/api/v1/queue/consulates/{consulate_id}/schedule"
appointment_params = {
    "date": today,
    "dateEnd": today,
    "serviceId": service_id
}

logging.basicConfig(filename=".log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logging.basicConfig(level=logging.INFO)

solver = TwoCaptcha(captcha_api_key)
session = requests.Session()


def solve_flare():
    fs_session = FSSession()
    json = fs_session.get(url)

    cookies = {cookie['name']: cookie['value'] for cookie in json['cookies']}
    user_agent = json['userAgent']

    session.headers = {"User-Agent": user_agent}
    session.cookies.update(cookies)


def solve_captcha():
    logging.info("Trying to solve captcha")
    s_time = time.time()
    try:
        result = solver.recaptcha(sitekey=sitekey, url=url)
    except Exception as e:
        raise Exception(f"Failed to solve captcha {str(e)}")
    logging.info(f"Captcha solved in {time.time() - s_time :.2f} sec")
    return result.get('code')


def authorize():
    token = solve_captcha()
    data = {
        "countryId": country_id,
        "g-recaptcha-response": token
    }

    response = session.post(session_url, data=data)
    if response.status_code != 200:
        raise Exception("Authorization failed")

    logging.info("Authorization successes")
    return response.json().get('token')


def get_appointment():
    logging.info("Trying to get appointments")
    response = session.get(appointment_url, params=appointment_params)
    if response.status_code != 200:
        logging.warning("Enable to get data")
        return None
    apps = response.json()
    logging.info(f"{len(apps)} appointments received")
    return apps


def play_sound():
    os.system("start wmplayer " + sound_path)


def new_session():
    logging.info("New session started")
    solve_flare()
    auth_key = authorize()
    session.headers["authorization"] = "Bearer " + auth_key
    while True:
        apps = get_appointment()
        if apps is None:
            break
        if len(apps) > 0:
            play_sound()
        time.sleep(delay)


if __name__ == "__main__":
    try:
        while True:
            new_session()
            time.sleep(delay)
    except Exception as e:
        logging.critical(str(e))
        exit()
