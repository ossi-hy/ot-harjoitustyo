from typing import Optional
import numpy as np
from pool import PiecePool

SHAPES = [
    np.array([[0, 1, 0], [1, 1, 1]]),
    np.array([[0, 2, 2], [2, 2, 0]]),
    np.array([[3, 3, 0], [0, 3, 3]]),
    np.array([[4, 0, 0], [4, 4, 4]]),
    np.array([[0, 0, 5], [5, 5, 5]]),
    np.array([[6, 6, 6, 6]]),
    np.array([[7, 7], [7, 7]]),
]


class Board:
    def __init__(self, width=10, height=20, seed: Optional[int]=None) -> None:
        self.width = width
        self.height = height
        self.board = np.zeros((self.height, self.width), dtype=np.uint8)

        self.pool = PiecePool(seed)
        self.piece = self.pool.next_piece()

        print(SHAPES[self.piece].shape[1])
        self.piece_x = (
            4 - (SHAPES[self.piece].shape[1] + 1) // 2 + 1 # Offset the center position for different pieces
        )  # X-position of the currently dropping piece
        self.piece_y = 0  # Y-position of the currently dropping piece
        self.piece_r = 0  # Rotation of the currently dropping piece

    def get_board_with_piece(self) -> np.ndarray:
        shape = SHAPES[self.piece]
        new_board = np.copy(self.board)
        new_board[
            self.piece_y : self.piece_y + shape.shape[0],
            self.piece_x : self.piece_x + shape.shape[1],
        ] = shape
        return new_board

    def move(self, dir: int):
        if dir == 0: # Left
            if self.piece_x == 0:
                return
            self.piece_x -= 1
        elif dir == 1:
            if self.piece_x+SHAPES[self.piece].shape[1] == self.width:
                return
            self.piece_x += 1

    def rotate(self):
        pass

    def step(self):
        pass
