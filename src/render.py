import tkinter as tk

from board import Board

# Colors of the tetraminos
COLORS = [
    (0, 0, 0),
    (180, 0, 255),
    (0, 150, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 120, 0),
    (0, 220, 220),
    (255, 255, 0),
]


class Renderer:
    def __init__(self, window: tk.Tk, board: Board, width=300, height=600) -> None:
        self._window = window
        self.w = width
        self.h = height
        self._canvas = tk.Canvas(self._window, width=width, height=height)
        self._canvas.pack()
        self._board = board

    def draw(self) -> None:
        self._canvas.delete("all")

        self._draw_board()

        self._window.update()

    def _draw_board(self) -> None:
        for y in range(self._board.h):
            for x in range(self._board.w):
                color = "#{:02x}{:02x}{:02x}".format(*COLORS[self._board.board[y, x]])
                self._canvas.create_rectangle(
                    x * self.w / self._board.w,
                    y * self.h / self._board.h,
                    (x + 1) * self.w / self._board.w,
                    (y + 1) * self.h / self._board.h,
                    outline="#000000",
                    fill=color,
                )
