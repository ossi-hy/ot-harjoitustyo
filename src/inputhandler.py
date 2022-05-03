from __future__ import annotations

import keyboard as kb  # type: ignore
#from pynput import keyboard as kb
from board import Board
from config import Controls, DAS, ARR

class Action:
    LEFT = 0
    RIGHT = 1
    CW = 2
    CCW = 3
    UPSIDE_DOWN = 4
    DROP = 5
    HOLD = 6
    RESET = 7


class InputHandler:
    def __init__(self, board: Board) -> None:
        self._board = board
        self.das_timer = DAS
        self.arr_timer = ARR
        self.das_elapsed = False

        self.inputs = {
            Action.LEFT: Controls.LEFT,
            Action.RIGHT: Controls.RIGHT,
            Action.CW: Controls.CW,
            Action.CCW: Controls.CCW,
            Action.UPSIDE_DOWN: Controls.UPSIDE_DOWN,
            Action.DROP: Controls.DROP,
            Action.HOLD: Controls.HOLD,
            Action.RESET: Controls.RESET
        }

        self.pressed = {
            Controls.LEFT: False,
            Controls.RIGHT: False,
            Controls.CW: False,
            Controls.CCW: False,
            Controls.UPSIDE_DOWN: False,
            Controls.DROP: False,
            Controls.HOLD: False,
            Controls.RESET: False,
        }

    def process_inputs(self, elapsed: float) -> None:
        move_keys_pressed = False
        for action, key in self.inputs.items():
            if kb.is_pressed(key):
                # Key is already pressed
                if self.pressed[action]:
                    # It's a movement key
                    if action in (Action.LEFT, Action.RIGHT):
                        move_keys_pressed = True
                        self.calculate_das_arr(action, elapsed)
                    continue

                # Key is pressed first time
                if action == Action.LEFT or action == Action.RIGHT:
                    self.move(action)
                elif action == Action.CW:
                    self._board.rotate(0)
                elif action == Action.CCW:
                    self._board.rotate(1)
                elif action == Action.UPSIDE_DOWN:
                    self._board.rotate(2)
                elif action == Action.DROP:
                    self._board.drop()
                elif action == Action.HOLD:
                    self._board.hold()
                elif action == Action.RESET:
                    self._board.reset()
                # Mark the key is pressed
                self.pressed[action] = True
            # Key is not pressed or released
            else:
                # Reset DAS and ARR timers when movement keys are lifted
                self.pressed[action] = False
        if not move_keys_pressed:
            self.das_timer = DAS
            self.arr_timer = ARR
            self.das_elapsed = False

    def move(self, action: Action) -> None:
        if action == Action.LEFT:
            self._board.move(0)
        elif action == Action.RIGHT:
            self._board.move(1)

    def calculate_das_arr(self, action: Action, elapsed: float) -> None:
        if self.das_elapsed:
            self.arr_timer -= elapsed * 1000
            if self.arr_timer <= 0:
                self.move(action)
                self.arr_timer = ARR
        else:
            self.das_timer -= elapsed * 1000
            if self.das_timer <= 0:
                self.move(action)
                self.das_elapsed = True
