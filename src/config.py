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


control_names = {
    Action.LEFT: "move-left",
    Action.RIGHT: "move-right",
    Action.CW: "rotate-cw",
    Action.CCW: "rotate-ccw",
    Action.UPSIDE_DOWN: "rotate-180",
    Action.DROP: "drop",
    Action.HOLD: "hold",
    Action.RESET: "reset",
}

controls = {Action.BACK: "escape"}

for action, name in control_names.items():
    controls[action] = _parser["CONTROLS"][name]

DAS = _parser["GAMEPLAY"].getint("DAS")
ARR = _parser["GAMEPLAY"].getint("ARR")

SHADOW = _parser["GAMEPLAY"].getboolean("shadow")
