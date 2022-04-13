import configparser
import os

FILENAME = "settings.ini"
_dirname = os.path.dirname(__file__)

_parser = configparser.ConfigParser()
_parser.read(os.path.join(_dirname, "..", "config", FILENAME))

WINDOW_WIDTH = _parser["WINDOW"].getint("width")
WINDOW_HEIGHT = _parser["WINDOW"].getint("height")

class Controls:
    LEFT = _parser["CONTROLS"]["move-left"] or "left"
    RIGHT = _parser["CONTROLS"]["move-right"] or "right"
    CW = _parser["CONTROLS"]["rotate-cw"] or 'd'
    CCW = _parser["CONTROLS"]["rotate-ccw"] or 'a'
    UPSIDE_DOWN = _parser["CONTROLS"]["rotate-180"] or 's'
    DROP = _parser["CONTROLS"]["drop"] or "space"
    RESET = _parser["CONTROLS"]["reset"] or 'f'

DAS = _parser["GAMEPLAY"].getint("DAS")
ARR = _parser["GAMEPLAY"].getint("ARR")

SHADOW = _parser["GAMEPLAY"].getboolean("shadow")