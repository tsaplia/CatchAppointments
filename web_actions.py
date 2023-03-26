import logging
from datetime import date

import requests

from captcha import solve_captcha, url
from config import consulate_id, country_id, service_id
from flare_solverr import FSSession

session_url = "https://online.mfa.gov.ua/api/v1/auth/session"

today = date.today().strftime("%Y-%m-%d")
appointment_url = f"https://online.mfa.gov.ua/api/v1/queue/consulates/{consulate_id}/schedule"
appointment_params = {
    "date": today,
    "dateEnd": today,
    "serviceId": service_id
}

session = requests.Session()


def solve_flare():
    fs_session = FSSession()
    json = fs_session.get(url)

    cookies = {cookie['name']: cookie['value'] for cookie in json['cookies']}
    user_agent = json['userAgent']

    session.headers = {"User-Agent": user_agent}
    session.cookies.update(cookies)


def get_auth_token():
    recaptcha_response = solve_captcha()
    data = {
        "countryId": country_id,
        "g-recaptcha-response": recaptcha_response
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


def authorize():
    solve_flare()
    session.headers["authorization"] = "Bearer " + get_auth_token()
