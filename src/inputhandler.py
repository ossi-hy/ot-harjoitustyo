from __future__ import annotations

from pynput import keyboard as kb
from board import Board
from config import Action, Controls, DAS, ARR
import time



class InputHandler:
    def __init__(self, board: Board) -> None:
        self._board = board
        self.das_timer = DAS
        self.arr_timer = ARR
        self.das_elapsed = False

        self.actions = {}

        for action, key in Controls.items():
            if len(key) == 1:
                self.actions[kb.KeyCode(char=key)] = action
            else:
                self.actions[eval(f"kb.Key.{key}")] = action

        self.trigger = {
            Action.LEFT: False,
            Action.RIGHT: False,
            Action.CW: False,
            Action.CCW: False,
            Action.UPSIDE_DOWN: False,
            Action.DROP: False,
            Action.HOLD: False,
            Action.RESET: False,
            Action.BACK: False,
        }

        self.pressed = self.trigger.copy()
        self.listener = kb.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.input_time = time.perf_counter()

    def on_press(self, key):
        if key in self.actions:
            self.trigger[self.actions[key]] = True

    def on_release(self, key):
        if key in self.actions:
            self.trigger[self.actions[key]] = False

    def process_inputs(self, elapsed: float) -> bool:
        move_keys_pressed = False
        for action in self.trigger:
            if self.trigger[action]:
                if action == Action.BACK:
                    # Prevent reading immediately again
                    self.trigger[action] = False
                    return False
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

        return True

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
