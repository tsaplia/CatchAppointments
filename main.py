import logging
import time

from alarm import play_sound
from config import delay
from web_actions import authorize, get_appointment

logging.basicConfig(filename=".log",
                    filemode='a',
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logging.basicConfig(level=logging.INFO)


def new_session():
    logging.info("New session started")
    authorize()
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
