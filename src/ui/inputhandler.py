from __future__ import annotations
import time
import tkinter as tk
from game.board import Board
from config import Action, controls, DAS, ARR, write_control
import ui.render


class InputHandler:
    def __init__(self, window: tk.Tk, board: Board) -> None:
        """Inputhandler handles keyboard inputs

        Args:
            window (tk.Tk): Window to get inputs from
            board (Board): Board that is currently being played on
        """
        self._window = window

        self._board = board
        self.das_timer = DAS
        self.arr_timer = ARR
        self.das_elapsed = False

        self.actions = {}
        self.create_actions()

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

        window.bind("<KeyPress>", self.on_press)
        window.bind("<KeyRelease>", self.on_release)

    def create_actions(self):
        """Create/update the key->action map
        """
        self.actions = {}
        for action, key in controls.items():
            self.actions[key] = action


    def on_press(self, key: tk.Event) -> None:
        """Keypress callback function

        Args:
            key (kb.Key/kb.KeyCode/None): Pressed key
        """
        key = key.keysym.lower()
        if key in self.actions:
            self.trigger[self.actions[key]] = True

    def on_release(self, key: tk.Event) -> None:
        """Keyrelease callback function

        Args:
            key (kb.Key/kb.KeyCode/None): Released key
        """
        key = key.keysym.lower()
        if key in self.actions:
            self.trigger[self.actions[key]] = False

    def process_inputs(self, renderer: ui.render.Renderer, elapsed: float) -> None:
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
                if renderer.state == ui.render.State.MAINMENU:
                    renderer.state = ui.render.State.EXIT
                else:
                    renderer.state = ui.render.State.MAINMENU
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
                renderer.reset_gametime()
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

    def on_record_press(self, key: tk.Event, renderer: ui.render.Renderer):
        """Keypress callback function when rebinding controls

        Args:
            key (tk.Event): Key being pressed
            renderer (ui.render.Renderer): renderer to redraw settings menu
        """
        key = key.keysym.lower()

        if key in self.actions:
            if self.actions[key] == Action.BACK:
                self._window.unbind("<KeyPress>")
                self._window.bind("<KeyPress>", self.on_press)
                renderer._draw_settings()
                return

        write_control(self.recording_action, key)
        self.create_actions()

        self._window.unbind("<KeyPress>")
        self._window.bind("<KeyPress>", self.on_press)

        renderer._draw_settings()

    def record_key(self, action: Action, renderer: ui.render.Renderer):
        """Starts listening for key rebinding

        Args:
            action (Action): Action to rebind
            renderer (ui.render.Renderer): renderer to redraw settings menu
        """
        self._window.unbind("<KeyPress>")

        self.recording_action = action

        self._window.bind("<KeyPress>", lambda x, y=renderer: self.on_record_press(x, y))