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
        self._das_timer = DAS
        self._arr_timer = ARR
        self._das_elapsed = False

        self._actions = {}
        self._create_actions()

        self._trigger = {
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

        self._pressed = self._trigger.copy()

        window.bind("<KeyPress>", self._on_press)
        window.bind("<KeyRelease>", self._on_release)

    def _create_actions(self):
        """Create/update the key->action map
        """
        self._actions = {}
        for action, key in controls.items():
            self._actions[key] = action


    def _on_press(self, key: tk.Event) -> None:
        """Keypress callback function

        Args:
            key (kb.Key/kb.KeyCode/None): Pressed key
        """
        key = key.keysym.lower()
        if key in self._actions:
            self._trigger[self._actions[key]] = True

    def _on_release(self, key: tk.Event) -> None:
        """Keyrelease callback function

        Args:
            key (kb.Key/kb.KeyCode/None): Released key
        """
        key = key.keysym.lower()
        if key in self._actions:
            self._trigger[self._actions[key]] = False

    def process_inputs(self, renderer: ui.render.Renderer, elapsed: float) -> None:
        """Process inputs since the last frame

        Args:
            renderer (Renderer): Renderer to send control signals to
            elapsed (float): Time since last time this function was called
        """
        move_keys_pressed = False
        for action, trigger in self._trigger.items():
            if not trigger:
                self._pressed[action] = False
                continue
            if action == Action.BACK:
                # Prevent reading immediately again
                self._trigger[action] = False
                if renderer.state == ui.render.State.MAINMENU:
                    renderer.state = ui.render.State.EXIT
                else:
                    renderer.state = ui.render.State.MAINMENU
                return
            # Key is already pressed
            if self._pressed[action]:
                # It's a movement key
                if action in (Action.LEFT, Action.RIGHT):
                    move_keys_pressed = True
                    self._calculate_das_arr(action, elapsed)
                continue

            # Key is pressed first time
            if action in (Action.LEFT, Action.RIGHT):
                self._move(action)
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
                renderer._reset_gametime()
                self._board.reset()

            self._pressed[action] = True
        # Reset DAS and ARR timers when movement keys are lifted
        if not move_keys_pressed:
            self._das_timer = DAS
            self._arr_timer = ARR
            self._das_elapsed = False

    def _move(self, action: Action) -> None:
        """Small helper function to seperate left and right movements

        Args:
            action (Action): _description_
        """
        if action == Action.LEFT:
            self._board.move(0)
        elif action == Action.RIGHT:
            self._board.move(1)

    def _calculate_das_arr(self, action: Action, elapsed: float) -> None:
        """Keep track of the das and arr timers, and move piece accordingly

        Args:
            action (Action): Move left or right
            elapsed (float): Time since input processing was last called
        """
        if self._das_elapsed:
            self._arr_timer -= elapsed * 1000
            if self._arr_timer <= 0:
                self._move(action)
                self._arr_timer = ARR
        else:
            self._das_timer -= elapsed * 1000
            if self._das_timer <= 0:
                self._move(action)
                self._das_elapsed = True

    def _on_record_press(self, key: tk.Event, renderer: ui.render.Renderer):
        """Keypress callback function when rebinding controls

        Args:
            key (tk.Event): Key being pressed
            renderer (ui.render.Renderer): renderer to redraw settings menu
        """
        key = key.keysym.lower()

        if key in self._actions:
            if self._actions[key] == Action.BACK:
                self._window.unbind("<KeyPress>")
                self._window.bind("<KeyPress>", self._on_press)
                renderer._draw_settings()
                return

        write_control(self.recording_action, key)
        self._create_actions()

        self._window.unbind("<KeyPress>")
        self._window.bind("<KeyPress>", self._on_press)

        renderer._draw_settings()

    def record_key(self, action: Action, renderer: ui.render.Renderer):
        """Starts listening for key rebinding

        Args:
            action (Action): Action to rebind
            renderer (ui.render.Renderer): renderer to redraw settings menu
        """
        self._window.unbind("<KeyPress>")

        self.recording_action = action

        self._window.bind("<KeyPress>", lambda x, y=renderer: self._on_record_press(x, y))