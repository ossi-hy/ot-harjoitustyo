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
        self.width = width
        self.height = height
        self._canvas = tk.Canvas(self._window, width=width, height=height)
        self._canvas.pack()
        self._board = board
        self.grid = []

        self._build_grid()

    def draw(self) -> None:
        #self._canvas.delete("all")

        self._draw_board()

        self._window.update()

    def _build_grid(self) -> None:
        for row in range(self._board.visible_height):
            row_rects = []
            for col in range(self._board.width):
                color = "#{:02x}{:02x}{:02x}".format(*COLORS[0])
                rect = self._canvas.create_rectangle(
                    col * self.width / self._board.width,
                    row * self.height / self._board.visible_height,
                    (col + 1) * self.width / self._board.width,
                    (row + 1) * self.height / self._board.visible_height,
                    outline="#000000",
                    fill=color,
                )
                row_rects.append(rect)
            self.grid.append(row_rects)

    def _draw_board(self) -> None:
        offset = self._board.height - self._board.visible_height
        for row in range(self._board.visible_height):
            for col in range(self._board.width):
                color = "#{:02x}{:02x}{:02x}".format(
                    *COLORS[self._board.get_board_with_piece()[row + offset, col]]
                )
                self._canvas.itemconfig(self.grid[row][col], fill=color)