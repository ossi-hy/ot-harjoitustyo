from __future__ import annotations
import configparser
import os

FILENAME = "settings.ini"
_dirname = os.path.dirname(__file__)

_parser = configparser.ConfigParser()
_parser.read(os.path.join(_dirname, "..", "config", FILENAME))

WINDOW_WIDTH = _parser["WINDOW"].getint("width")
WINDOW_HEIGHT = _parser["WINDOW"].getint("height")


class Action:
    LEFT = 0
    RIGHT = 1
    CW = 2
    CCW = 3
    UPSIDE_DOWN = 4
    DROP = 5
    HOLD = 6
    RESET = 7

Controls = {
    Action.LEFT: _parser["CONTROLS"]["move-left"] or "left",
    Action.RIGHT: _parser["CONTROLS"]["move-right"] or "right",
    Action.CW: _parser["CONTROLS"]["rotate-cw"] or 'd',
    Action.CCW: _parser["CONTROLS"]["rotate-ccw"] or 'a',
    Action.UPSIDE_DOWN: _parser["CONTROLS"]["rotate-180"] or 's',
    Action.DROP: _parser["CONTROLS"]["drop"] or "space",
    Action.HOLD: _parser["CONTROLS"]["hold"] or "up",
    Action.RESET: _parser["CONTROLS"]["reset"] or 'f'
}

DAS = _parser["GAMEPLAY"].getint("DAS")
ARR = _parser["GAMEPLAY"].getint("ARR")

SHADOW = _parser["GAMEPLAY"].getboolean("shadow")
