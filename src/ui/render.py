from __future__ import annotations
import tkinter as tk
import time
from enum import Enum, auto

from game.board import Board
from game.piece import SHAPES
import ui.inputhandler
import config

# Colors of the tetrominos
COLORS = [
    (10, 10, 10),
    (180, 0, 255),
    (0, 150, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 120, 0),
    (0, 220, 220),
    (255, 255, 0),
    (100, 100, 100),
]

# Possible states of the game
class State(Enum):
    MAINMENU = auto()
    SETTINGS = auto()
    GAME = auto()
    GAME_OVER = auto()
    EXIT = auto()


class Renderer:
    GAME_PADDING_RIGHT = 1.6

    def __init__(
        self, window: tk.Tk, board: Board, inputhandler: ui.inputhandler.InputHandler
    ) -> None:
        """Creates renderer to draw all the menus and game on the window

        Args:
            window (tk.Tk): window to be drawn to
            board (Board): board to draw when playing the game
            inputhandler (ui.inputhandler.InputHandler): inputhandler for the given window
        """
        self._window = window
        self._inputhandler = inputhandler
        self.width = config.WINDOW_WIDTH
        self.height = config.WINDOW_HEIGHT
        self._canvas = tk.Canvas(self._window, width=self.width, height=self.height)
        self._canvas.pack()
        self._board = board
        self._grid = []
        self._hold_grid = []
        self._last_state = -1
        self.state = State.MAINMENU
        self.gametime = 0
        # Game info texts
        self._clr_txt = None
        self._tmr_txt = None

    def _reset_gametime(self):
        """Reset gametime. Should be called after reseting the game
        """
        self.gametime = time.time()

    def draw(self) -> bool:
        """The main function to be called every frame. Handles state transitions and calls drawing functions.

        Returns:
            bool: Returns False if the state is 'Exit' meaning the window should be closed
        """
        if self.state == State.MAINMENU:
            if self._last_state != self.state:
                self._draw_mainmenu()
        elif self.state == State.SETTINGS:
            if self._last_state != self.state:
                self._draw_settings()
        elif self.state == State.GAME:
            if self._last_state != self.state:
                self._board.reset()
                self._build_grid()
                self.gametime = time.time()
                self._draw_game_info()
            self._draw_board()
            self._update_game_info()
            if self._board.over:
                self.gametime = time.time() - self.gametime
                self.state = State.GAME_OVER
                return True
        elif self.state == State.GAME_OVER:
            if self._last_state != self.state:
                self._draw_game_over()
        elif self.state == State.EXIT:
            return False

        self._last_state = self.state

        self._window.update()

        return True

    def _draw_mainmenu(self) -> None:
        """Draws the main menu of the program"""
        self._canvas.delete("all")

        self._canvas.create_text(
            self.width / 2, self.height / 8, text="TETRIS", font=("Arial", 54)
        )

        play_btn = self._canvas.create_rectangle(
            self.width / 6,
            self.height / 4,
            self.width - self.width / 6,
            self.height / 4 + self.height / 5,
            fill="white",
        )
        play_txt = self._canvas.create_text(
            self.width / 2,
            self.height / 4 + self.height / 10,
            text="Play",
            font=("Arial", 54),
        )
        self._canvas.tag_bind(play_btn, "<Button-1>", self._click_play)
        self._canvas.tag_bind(play_txt, "<Button-1>", self._click_play)

        stn_btn = self._canvas.create_rectangle(
            self.width / 6,
            self.height / 2,
            self.width - self.width / 6,
            self.height / 2 + self.height / 5,
            fill="white",
        )
        stn_txt = self._canvas.create_text(
            self.width / 2,
            self.height / 2 + self.height / 10,
            text="Settings",
            font=("Arial", 54),
        )
        self._canvas.tag_bind(stn_btn, "<Button-1>", self._click_settings)
        self._canvas.tag_bind(stn_txt, "<Button-1>", self._click_settings)

        exit_btn = self._canvas.create_rectangle(
            self.width / 6,
            3 * self.height / 4,
            self.width - self.width / 6,
            3 * self.height / 4 + self.height / 5,
            fill="white",
        )
        exit_txt = self._canvas.create_text(
            self.width / 2,
            3 * self.height / 4 + self.height / 10,
            text="Exit",
            font=("Arial", 54),
        )
        self._canvas.tag_bind(exit_btn, "<Button-1>", self._click_exit)
        self._canvas.tag_bind(exit_txt, "<Button-1>", self._click_exit)

    def _draw_settings(self, hide: config.Action = None) -> None:
        """Draw the settings menu where you can rebind controls and toggle piece shadow

        Args:
            hide (Action, optional): Hide the key that is currently waiting for keypress. Defaults to None.
        """
        self._canvas.delete("all")

        V_PAD = 160
        for i, (action, name) in enumerate(config.control_names.items()):
            self._canvas.create_rectangle(
                self.width / 12 - 10,
                i * (self.height - V_PAD * 2) / 8 + 36,
                self.width / 12 + 100,
                i * (self.height - V_PAD * 2) / 8 + 64,
                fill="white",
            )
            self._canvas.create_text(
                self.width / 12,
                i * (self.height - V_PAD * 2) / 8 + 40,
                anchor="nw",
                text=name,
                font=("Arial", 12),
            )
            key_rec = self._canvas.create_rectangle(
                self.width / 2.5 - 10,
                i * (self.height - V_PAD * 2) / 8 + 36,
                self.width / 2.5 + 100,
                i * (self.height - V_PAD * 2) / 8 + 64,
                fill="white",
            )
            if action == hide:
                continue
            key_txt = self._canvas.create_text(
                self.width / 2.5,
                i * (self.height - V_PAD * 2) / 8 + 40,
                anchor="nw",
                text=config.controls[action],
                font=("Arial", 12),
            )
            self._canvas.tag_bind(
                key_rec, "<Button-1>", lambda x, y=action: self._click_bind(x, y)
            )
            self._canvas.tag_bind(
                key_txt, "<Button-1>", lambda x, y=action: self._click_bind(x, y)
            )

        self._canvas.create_rectangle(
            self.width / 12 - 10,
            10 * (self.height - V_PAD * 2) / 8 + 36,
            self.width / 12 + 100,
            10 * (self.height - V_PAD * 2) / 8 + 64,
            fill="white",
        )
        self._canvas.create_text(
            self.width / 12,
            10 * (self.height - V_PAD * 2) / 8 + 40,
            anchor="nw",
            text="shadow",
            font=("Arial", 12),
        )
        shd_rec = self._canvas.create_rectangle(
            self.width / 2.5 - 10,
            10 * (self.height - V_PAD * 2) / 8 + 36,
            self.width / 2.5 + 100,
            10 * (self.height - V_PAD * 2) / 8 + 64,
            fill="white",
        )
        shd_txt = self._canvas.create_text(
            self.width / 2.5,
            10 * (self.height - V_PAD * 2) / 8 + 40,
            anchor="nw",
            text="true" if config.SHADOW else "false",
            font=("Arial", 12),
        )
        self._canvas.tag_bind(shd_rec, "<Button-1>", self._click_shadowtoggle)
        self._canvas.tag_bind(shd_txt, "<Button-1>", self._click_shadowtoggle)

    def _click_play(self, event: tk.Event) -> None:
        """Callback function for clicking play button on main menu

        Args:
            event (tk.Event): _description_
        """
        self.state = State.GAME

    def _click_settings(self, event: tk.Event) -> None:
        """Callback function for clicking settings button on main menu

        Args:
            event (tk.Event): _description_
        """
        self.state = State.SETTINGS

    def _click_bind(self, event: tk.Event, action: config.Action):
        """Callback function for clicking any key to rebind

        Args:
            event (tk.Event): _description_
            action (config.Action): Action to be rebound
        """
        self._inputhandler.record_key(action, self)
        self._draw_settings(action)

    def _click_shadowtoggle(self, event: tk.Event):
        """Callback function to be called when user clicked to toggle the shadow

        Args:
            event (tk.Event): _description_
        """
        config.toggle_shadow()
        self._draw_settings()

    def _click_exit(self, event: tk.Event) -> None:
        """Callback function for clikcing exit button on main menu

        Args:
            event (tk.Event): _description_
        """
        self.state = State.EXIT

    def _build_grid(self) -> None:
        """Builds the tetris grid and additional small grid for held piece"""
        # Clear the grids
        self._grid = []
        self._hold_grid = []
        # Clear the screen
        self._canvas.delete("all")

        game_width = self.width / self.GAME_PADDING_RIGHT
        for row in range(self._board.visible_height):
            row_rects = []
            for col in range(self._board.width):
                color = "#{:02x}{:02x}{:02x}".format(*COLORS[0])
                rect = self._canvas.create_rectangle(
                    col * game_width / self._board.width,
                    row * self.height / self._board.visible_height,
                    (col + 1) * game_width / self._board.width,
                    (row + 1) * self.height / self._board.visible_height,
                    outline="#000000",
                    fill=color,
                )
                row_rects.append(rect)
            self._grid.append(row_rects)
        for row in range(1, 5):
            row_rects = []
            for col in range(1, 5):
                color = "#{:02x}{:02x}{:02x}".format(*COLORS[0])
                rect = self._canvas.create_rectangle(
                    col * game_width / self._board.width + game_width,
                    row * self.height / self._board.visible_height,
                    (col + 1) * game_width / self._board.width + game_width,
                    (row + 1) * self.height / self._board.visible_height,
                    outline="#000000",
                    fill=color,
                )
                row_rects.append(rect)
            self._hold_grid.append(row_rects)

    def _draw_board(self) -> None:
        """Draws the current board and held piece"""
        offset = self._board.height - self._board.visible_height
        for row in range(self._board.visible_height):
            for col in range(self._board.width):
                color = "#{:02x}{:02x}{:02x}".format(
                    *COLORS[self._board.get_board_with_piece()[row + offset, col]]
                )
                self._canvas.itemconfig(self._grid[row][col], fill=color)
        # Draw held piece
        if self._board.hold_id == -1:
            return
        shape = SHAPES[self._board.hold_id - 1]
        for row in range(4):
            for col in range(4):
                if row < shape.shape[0] and col < shape.shape[1]:
                    color = "#{:02x}{:02x}{:02x}".format(*COLORS[shape[row, col]])
                else:
                    color = "#{:02x}{:02x}{:02x}".format(*COLORS[0])
                self._canvas.itemconfig(self._hold_grid[row][col], fill=color)

    def _draw_game_info(self) -> None:
        """Draw info about lines cleared and time elapsed
        """
        game_width = self.width / self.GAME_PADDING_RIGHT
        self._clr_txt = self._canvas.create_text(
            0.7 * game_width / self._board.width + game_width,
            self.height / 3,
            text=f"Cleared lines: {self._board.cleared}/{config.LINES}",
            font=("Arial", 12),
            anchor="nw",
        )
        self._tmr_txt = self._canvas.create_text(
            0.7 * game_width / self._board.width + game_width,
            self.height / 2,
            text=f"Time: {0.0}s",
            font=("Arial", 12),
            anchor="nw"
        )

    def _update_game_info(self) -> None:
        """Update lines cleared and time elapsed texts
        """
        self._canvas.itemconfig(self._clr_txt, text=f"Cleared lines: {self._board.cleared}/{config.LINES}")
        self._canvas.itemconfig(self._tmr_txt, text=f"Time: {time.time()-self.gametime:.2f}s",)

    def _draw_game_over(self) -> None:
        """Draw the game over screen
        """
        self._canvas.delete("all")
        self._canvas.create_text(
            self.width / 2, self.height / 2 - 100, text="Game Over!", font=("Arial", 36)
        )
        self._canvas.create_text(
            self.width / 2, self.height /2, text=f"Time: {self.gametime:.2f}s", font=("Arial", 24)
        )
        self._canvas.create_text(
            self.width / 2,
            self.height / 2 + 100,
            text=f"Lines cleared: {self._board.cleared}/{config.LINES}",
            font=("Arial", 24),
        )
