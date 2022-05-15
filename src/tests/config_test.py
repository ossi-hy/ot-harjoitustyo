import unittest
from importlib import reload
import config

class TestConfig(unittest.TestCase):
    def test_shadow_toggle(self):
        value = config.SHADOW
        config.toggle_shadow()
        reload(config)
        self.assertNotEqual(value, config.SHADOW)

        config.toggle_shadow()

    def test_write_control(self):
        left_key = config.controls[config.Action.LEFT]
        config.write_control(config.Action.LEFT, "a")
        reload(config)
        self.assertNotEqual(left_key, "a")

        config.write_control(config.Action.LEFT, left_key)

        