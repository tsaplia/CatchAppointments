import os

from config import sound_name

sound_path = f"{os.getcwd()}\\{sound_name}"


def play_sound():
    os.system("start wmplayer " + sound_path)
