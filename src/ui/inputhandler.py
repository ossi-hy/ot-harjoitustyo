from __future__ import annotations
import time
from pynput import keyboard as kb  # type: ignore
from game.board import Board
from config import Action, Controls, DAS, ARR
from ui.render import Renderer, State


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

    def on_press(self, key) -> None:
        """Keypress callback function

        Args:
            key (kb.Key/kb.KeyCode/None): Pressed key
        """
        if key in self.actions:
            self.trigger[self.actions[key]] = True

    def on_release(self, key) -> None:
        """Keyrelease callback function

        Args:
            key (kb.Key/kb.KeyCode/None): Released key
        """
        if key in self.actions:
            self.trigger[self.actions[key]] = False

    def process_inputs(self, renderer: Renderer, elapsed: float) -> None:
        """Process inputs since the last frame

        Args:
            renderer (Renderer): Renderer to send control signals to
            elapsed (float): Time since last time this function was called
        """
        move_keys_pressed = False
        for action, trigger in self.trigger.items():
            if not trigger:
                self.pressed[action] = False
                continue
            if action == Action.BACK:
                # Prevent reading immediately again
                self.trigger[action] = False
                if renderer.state == State.MAINMENU:
                    renderer.state = State.EXIT
                else:
                    renderer.state = State.MAINMENU
                return
            # Key is already pressed
            if self.pressed[action]:
                # It's a movement key
                if action in (Action.LEFT, Action.RIGHT):
                    move_keys_pressed = True
                    self.calculate_das_arr(action, elapsed)
                continue

            # Key is pressed first time
            if action in (Action.LEFT, Action.RIGHT):
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

            self.pressed[action] = True
        # Reset DAS and ARR timers when movement keys are lifted
        if not move_keys_pressed:
            self.das_timer = DAS
            self.arr_timer = ARR
            self.das_elapsed = False

    def move(self, action: Action) -> None:
        """Small helper function to seperate left and right movements

        Args:
            action (Action): _description_
        """
        if action == Action.LEFT:
            self._board.move(0)
        elif action == Action.RIGHT:
            self._board.move(1)

    def calculate_das_arr(self, action: Action, elapsed: float) -> None:
        """Keep track of the das and arr timers, and move piece accordingly

        Args:
            action (Action): Move left or right
            elapsed (float): Time since input processing was last called
        """
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
