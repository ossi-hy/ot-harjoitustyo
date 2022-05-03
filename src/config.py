from __future__ import annotations
import configparser
import os
from enum import Enum, auto

FILENAME = "settings.ini"
_dirname = os.path.dirname(__file__)

_parser = configparser.ConfigParser()
_parser.read(os.path.join(_dirname, "..", "config", FILENAME))

WINDOW_WIDTH = _parser["WINDOW"].getint("width")
WINDOW_HEIGHT = _parser["WINDOW"].getint("height")


class Action(Enum):
    LEFT = auto()
    RIGHT = auto()
    CW = auto()
    CCW = auto()
    UPSIDE_DOWN = auto()
    DROP = auto()
    HOLD = auto()
    RESET = auto()
    BACK = auto()

Controls = {
    Action.LEFT: _parser["CONTROLS"]["move-left"] or "left",
    Action.RIGHT: _parser["CONTROLS"]["move-right"] or "right",
    Action.CW: _parser["CONTROLS"]["rotate-cw"] or 'd',
    Action.CCW: _parser["CONTROLS"]["rotate-ccw"] or 'a',
    Action.UPSIDE_DOWN: _parser["CONTROLS"]["rotate-180"] or 's',
    Action.DROP: _parser["CONTROLS"]["drop"] or "space",
    Action.HOLD: _parser["CONTROLS"]["hold"] or "up",
    Action.RESET: _parser["CONTROLS"]["reset"] or 'f',
    Action.BACK: "esc",
}

DAS = _parser["GAMEPLAY"].getint("DAS")
ARR = _parser["GAMEPLAY"].getint("ARR")

SHADOW = _parser["GAMEPLAY"].getboolean("shadow")
