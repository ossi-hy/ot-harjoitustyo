from __future__ import annotations
import tkinter as tk


from board import Board
from piece import SHAPES
from config import WINDOW_WIDTH, WINDOW_HEIGHT

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

        #self._build_grid()

    def draw(self) -> None:
        if self.state == State.MAINMENU:
            if self.last_state != self.state:
                self._canvas.delete("all")
                self._draw_mainmenu()
        elif self.state == State.SETTINGS:
            pass
        elif self.state == State.GAME:
            if self.last_state != self.state:
                self._build_grid()
            self._draw_board()
        elif self.state == State.EXIT:
            return False

        self.last_state = self.state

        self._window.update()

        return True


    def _draw_mainmenu(self) -> None:
        self._canvas.create_text(self.width/2, self.height/8, text="TETRIS", font=("Arial", 54))

        play_btn = self._canvas.create_rectangle(
            self.width / 6,
            self.height / 4,
            self.width - self.width / 6,
            self.height / 4 + self.height / 5,
            fill="white",
        )
        play_txt = self._canvas.create_text(self.width/2, self.height/4+self.height/10, text="Play", font=("Arial", 54))
        self._canvas.tag_bind(play_btn, "<Button-1>", self.click_play)
        self._canvas.tag_bind(play_txt, "<Button-1>", self.click_play)

        stn_btn = self._canvas.create_rectangle(
            self.width / 6,
            self.height / 2,
            self.width - self.width / 6,
            self.height / 2 + self.height / 5,
            fill="white",
        )
        stn_txt = self._canvas.create_text(self.width/2, self.height/2+self.height/10, text="Settings", font=("Arial", 54))

        exit_btn = self._canvas.create_rectangle(
            self.width / 6,
            3*self.height / 4,
            self.width - self.width / 6,
            3*self.height / 4 + self.height / 5,
            fill="white",
        )
        exit_txt = self._canvas.create_text(self.width/2, 3*self.height/4+self.height/10, text="Exit", font=("Arial", 54))
        self._canvas.tag_bind(exit_btn, "<Button-1>", self.click_exit)
        self._canvas.tag_bind(exit_txt, "<Button-1>", self.click_exit)

    def click_play(self, event: tk.Event) -> None:
        self.state = State.GAME

    def click_exit(self, event: tk.Event) -> None:
        self.state = State.EXIT

    def _build_grid(self) -> None:
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
        for row in range(1,5):
            row_rects = []
            for col in range(1,5):
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
        offset = self._board.height - self._board.visible_height
        for row in range(self._board.visible_height):
            for col in range(self._board.width):
                color = "#{:02x}{:02x}{:02x}".format(
                    *COLORS[self._board.get_board_with_piece()[row + offset, col]]
                )
                self._canvas.itemconfig(self.grid[row][col], fill=color)
        if self._board.hold_id == -1:
            return
        shape = SHAPES[self._board.hold_id-1]
        for row in range(4):
            for col in range(4):
                if row < shape.shape[0] and col < shape.shape[1]:
                    color = "#{:02x}{:02x}{:02x}".format(
                        *COLORS[shape[row, col]]
                    )
                else:
                    color = "#{:02x}{:02x}{:02x}".format(
                        *COLORS[0]
                    )
                self._canvas.itemconfig(self.hold_grid[row][col], fill=color)
