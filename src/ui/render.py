from __future__ import annotations
import tkinter as tk


from game.board import Board
from game.piece import SHAPES
from config import WINDOW_WIDTH, WINDOW_HEIGHT, control_names, controls

# Colors of the tetraminos
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


class State:
    MAINMENU = 0
    SETTINGS = 1
    GAME = 2
    EXIT = 3


class Renderer:
    GAME_PADDING_RIGHT = 1.6

    def __init__(self, window: tk.Tk, board: Board) -> None:
        self._window = window
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self._canvas = tk.Canvas(self._window, width=self.width, height=self.height)
        self._canvas.pack()
        self._board = board
        self.grid = []
        self.hold_grid = []
        self.last_state = -1
        self.state = State.MAINMENU

    def draw(self) -> bool:
        """The main function to be called every frame. Handles state transitions and calls drawing functions.

        Returns:
            bool: Returns False if the state is 'Exit' meaning the window should be closed
        """
        if self.state == State.MAINMENU:
            if self.last_state != self.state:
                self._draw_mainmenu()
        elif self.state == State.SETTINGS:
            if self.last_state != self.state:
                self._draw_settings()
        elif self.state == State.GAME:
            if self.last_state != self.state:
                self._board.reset()
                self._build_grid()
            self._draw_board()
        elif self.state == State.EXIT:
            return False

        self.last_state = self.state

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

    def _draw_settings(self) -> None:
        self._canvas.delete("all")

        V_PAD = 160
        for i, (action, name) in enumerate(control_names.items()):
            self._canvas.create_rectangle(
                self.width / 12 - 10,
                i * (self.height - V_PAD * 2) / 8 + 36,
                self.width / 12 + 100,
                i * (self.height - V_PAD * 2) / 8 + 64,
                fill="white"
            )
            self._canvas.create_text(
                self.width / 12,
                i * (self.height - V_PAD * 2) / 8 + 40,
                anchor="nw",
                text=name,
                font=("Arial", 12),
            )
            self._canvas.create_rectangle(
                self.width / 2.5 - 10,
                i * (self.height - V_PAD * 2) / 8 + 36,
                self.width / 2.5 + 100,
                i * (self.height - V_PAD * 2) / 8 + 64,
                fill="white"
            )
            self._canvas.create_text(
                self.width / 2.5,
                i * (self.height - V_PAD * 2) / 8 + 40,
                anchor="nw",
                text=controls[action],
                font=("Arial", 12),
            )

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

    def _click_exit(self, event: tk.Event) -> None:
        """Callback function for clikcing exit button on main menu

        Args:
            event (tk.Event): _description_
        """
        self.state = State.EXIT

    def _build_grid(self) -> None:
        """Builds the tetris grid and additional small grid for held piece"""
        # Clear the grids
        self.grid = []
        self.hold_grid = []
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
            self.grid.append(row_rects)
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
            self.hold_grid.append(row_rects)

    def _draw_board(self) -> None:
        """Draws the current board and held piece"""
        offset = self._board.height - self._board.visible_height
        for row in range(self._board.visible_height):
            for col in range(self._board.width):
                color = "#{:02x}{:02x}{:02x}".format(
                    *COLORS[self._board.get_board_with_piece()[row + offset, col]]
                )
                self._canvas.itemconfig(self.grid[row][col], fill=color)
        if self._board.hold_id == -1:
            return
        shape = SHAPES[self._board.hold_id - 1]
        for row in range(4):
            for col in range(4):
                if row < shape.shape[0] and col < shape.shape[1]:
                    color = "#{:02x}{:02x}{:02x}".format(*COLORS[shape[row, col]])
                else:
                    color = "#{:02x}{:02x}{:02x}".format(*COLORS[0])
                self._canvas.itemconfig(self.hold_grid[row][col], fill=color)
