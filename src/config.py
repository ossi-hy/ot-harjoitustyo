import configparser
import os

FILENAME = "settings.ini"
_dirname = os.path.dirname(__file__)

_parser = configparser.ConfigParser()
_parser.read(os.path.join(_dirname, "..", "config", FILENAME))

WINDOW_WIDTH = int(_parser["WINDOW"]["width"])
WINDOW_HEIGHT = int(_parser["WINDOW"]["height"])

class Controls:
    LEFT = _parser["CONTROLS"]["move-left"] or "left"
    RIGHT = _parser["CONTROLS"]["move-right"] or "right"
    CW = _parser["CONTROLS"]["rotate-cw"] or 'd'
    CCW = _parser["CONTROLS"]["rotate-ccw"] or 'a'
    UPSIDE_DOWN = _parser["CONTROLS"]["rotate-180"] or 's'
    DROP = _parser["CONTROLS"]["drop"] or "space"