from __future__ import annotations
import configparser
import os
from enum import Enum, auto

FILENAME = "settings.ini"
_dirname = os.path.dirname(__file__)
_filepath = os.path.join(_dirname, "..", "config", FILENAME)

_parser = configparser.ConfigParser()
_parser.read(_filepath)

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

def write_control(action: Action, key: str):
    """Overrides new key in the config file

    Args:
        action (Action): Action to replace key for
        key (str): new key as str
    """
    _parser["CONTROLS"][control_names[action]] = key
    with open(_filepath, 'w', encoding="utf-8") as configfile:
        _parser.write(configfile)

    controls[action] = key

DAS = _parser["GAMEPLAY"].getint("das")
ARR = _parser["GAMEPLAY"].getint("arr")
LINES = _parser["GAMEPLAY"].getint("lines")

SHADOW = _parser["GAMEPLAY"].getboolean("shadow")

def toggle_shadow() -> None:
    """Toggle shadow and write it to config file
    """
    global SHADOW
    SHADOW = not SHADOW
    _parser["GAMEPLAY"]["shadow"] = 'true' if SHADOW else 'false'
    with open(_filepath, 'w', encoding="utf-8") as configfile:
        _parser.write(configfile)
