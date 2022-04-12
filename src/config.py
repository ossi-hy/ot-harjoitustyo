import configparser
import os

FILENAME = "settings.ini"
_dirname = os.path.dirname(__file__)

_parser = configparser.ConfigParser()
_parser.read(os.path.join(_dirname, "..", "config", FILENAME))

WINDOW_WIDTH = int(_parser["WINDOW"]["width"])
WINDOW_HEIGHT = int(_parser["WINDOW"]["height"])