from typing import Optional
import numpy as np
from pool import PiecePool
from piece import Piece

SHAPES = [
    np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]], dtype=np.uint8),
    np.array([[0, 2, 2], [2, 2, 0], [0, 0, 0]], dtype=np.uint8),
    np.array([[3, 3, 0], [0, 3, 3], [0, 0, 0]], dtype=np.uint8),
    np.array([[4, 0, 0], [4, 4, 4], [0, 0, 0]], dtype=np.uint8),
    np.array([[0, 0, 5], [5, 5, 5], [0, 0, 0]], dtype=np.uint8),
    np.array([[0, 0, 0, 0], [6, 6, 6, 6], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.uint8),
    np.array([[7, 7], [7, 7]], dtype=np.uint8),
]


class Board:
    def __init__(self, width=10, height=20, seed: Optional[int] = None) -> None:
        self.width = width
        self.height = height + 2
        self.visible_height = height

        self.board = np.zeros((self.height, self.width), dtype=np.uint8)

        self.piece = Piece(0,0,0,0)

        self.pool = PiecePool(seed)
        self.new_piece()

    def new_piece(self, piece_id: Optional[int] = None) -> None:
        piece_id = self.pool.next_piece() if piece_id is None else piece_id
        piece_x = (
            4
            - (SHAPES[piece_id - 1].shape[1] + 1) // 2
            + 1
        )
        piece_y = 2
        piece_r = 0
        self.piece = Piece(piece_id, piece_x, piece_y, piece_r)

    def get_board_with_piece(self) -> np.ndarray:
        shape, shape_left, shape_right, _ = self.piece.get_shape()
        new_board = np.copy(self.board)
        new_board[
            self.piece.y_pos : self.piece.y_pos + shape.shape[0],
            self.piece.x_pos + shape_left : self.piece.x_pos + shape.shape[1] - shape_right,
        ] = shape[:, shape_left : shape.shape[1] - shape_right]
        return new_board

    def move(self, direction: int) -> None:
        """Move the currently falling piece horizontally.

        Args:
            dir (int): 0 means left and 1 right
        """
        shape, shape_left, shape_right, _ = self.piece.get_shape()
        if direction == 0:
            if self.piece.x_pos <= 0 - shape_left:
                self.piece.x_pos = 0 - shape_left
                return
            self.piece.x_pos -= 1
        elif direction == 1:
            if self.piece.x_pos + shape.shape[1] - shape_right >= self.width:
                self.piece.x_pos = self.width - shape.shape[1] + shape_right
                return
            self.piece.x_pos += 1

    def rotate(self, direction: int) -> None:
        """Rotate the currently falling piece

        Args:
            dir (int): 0 means clockwise and 1 counterclockwise. 2 means rotate 180 degrees.
        """

        if direction == 0:
            self.piece.rotation -= 1
        elif direction == 1:
            self.piece.rotation += 1
        elif direction == 2:
            self.piece.rotation += 2

        # Perform wallkick
        shape, shape_left, shape_right, _ = self.piece.get_shape()
        if self.piece.x_pos + shape_left < 0:
            self.piece.x_pos -= self.piece.x_pos + shape_left
        if self.piece.x_pos + shape.shape[1] - shape_right > self.width:
            self.piece.x_pos += self.width + shape_right - self.piece.x_pos - shape.shape[1]

    def drop(self) -> None:
        shape, shape_left, shape_right, shape_bottom = self.piece.get_shape()
        for row in range(self.height, -1, -1):
            if row + shape.shape[0] - shape_bottom > self.height:
                continue
            strip_shape = shape[
                : shape.shape[1] - shape_bottom,
                shape_left : shape.shape[1] - shape_right,
            ]
            collision_area = self.board[
                row : row + strip_shape.shape[0],
                self.piece.x_pos + shape_left : self.piece.x_pos + shape.shape[1] - shape_right,
            ]
            if (collision_area[np.nonzero(strip_shape)] == 0).all():
                self.board[
                    row : row + strip_shape.shape[0],
                    self.piece.x_pos
                    + shape_left : self.piece.x_pos
                    + shape.shape[1]
                    - shape_right,
                ] += strip_shape
                self.clear_lines()
                self.new_piece()
                break

    def clear_lines(self) -> None:
        """Clear the complete lines
        """
        for row in range(self.height - 1, -1, -1):
            if (self.board[row] != 0).all():
                self.board[:row+1] = np.roll(self.board[:row+1], 1, axis=0)
                self.board[0] = np.zeros(self.width, dtype=np.uint8)

    def step(self):
        pass
