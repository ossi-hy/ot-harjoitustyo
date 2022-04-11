from typing import Optional
import numpy as np
from pool import PiecePool

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

        self.pool = PiecePool(seed)
        self.new_piece(id=0)

    def new_piece(self, id: Optional[int] = None) -> None:
        self.piece = self.pool.next_piece() if id == None else id
        self.piece_x = (
            4
            - (SHAPES[self.piece - 1].shape[1] + 1) // 2
            + 1  # Offset the center position for different pieces
        )  # X-position of the currently dropping piece
        self.piece_y = 2  # Y-position of the currently dropping piece
        self.piece_r = 0  # Rotation of the currently dropping piece

    def _get_shape(self) -> tuple[np.ndarray, int, int, int]:
        shape = SHAPES[self.piece - 1]
        shape = np.rot90(shape, self.piece_r)
        shape_left = shape.any(0).argmax()
        shape_right = np.fliplr(shape).any(0).argmax()
        shape_bottom = np.flipud(shape).any(1).argmax()
        return shape, shape_left, shape_right, shape_bottom

    def get_board_with_piece(self) -> np.ndarray:
        shape, shape_left, shape_right, _ = self._get_shape()
        new_board = np.copy(self.board)
        new_board[
            self.piece_y : self.piece_y + shape.shape[0],
            self.piece_x + shape_left : self.piece_x + shape.shape[1] - shape_right,
        ] = shape[:, shape_left : shape.shape[1] - shape_right]
        return new_board

    def move(self, dir: int) -> None:
        """Move the currently falling piece horizontally.

        Args:
            dir (int): 0 means left and 1 right
        """
        shape, shape_left, shape_right, _ = self._get_shape()
        if dir == 0:
            if self.piece_x <= 0 - shape_left:
                self.piece_x = 0 - shape_left
                return
            self.piece_x -= 1
        elif dir == 1:
            if self.piece_x + shape.shape[1] - shape_right >= self.width:
                self.piece_x = self.width - shape.shape[1] + shape_right
                return
            self.piece_x += 1

    def rotate(self, dir: int) -> None:
        """Rotate the currently falling piece

        Args:
            dir (int): 0 means clockwise and 1 counterclockwise. 2 means rotate 180 degrees.
        """

        if dir == 0:
            self.piece_r -= 1
        elif dir == 1:
            self.piece_r += 1
        elif dir == 2:
            self.piece_r += 2


        # Perform wallkick
        shape, shape_left, shape_right, _ = self._get_shape()
        if self.piece_x + shape_left < 0:
            self.piece_x -= self.piece_x + shape_left
        if self.piece_x + shape.shape[1] - shape_right > self.width:
            self.piece_x += self.width + shape_right - self.piece_x - shape.shape[1]

    def drop(self) -> None:
        shape, shape_left, shape_right, shape_bottom = self._get_shape()
        for row in range(self.height, -1, -1):
            print(row+shape.shape[0]-shape_bottom)
            if row+shape.shape[0]-shape_bottom > self.height:
                continue
            strip_shape = shape[
                : shape.shape[1] - shape_bottom,
                shape_left : shape.shape[1] - shape_right,
            ]
            collision_area = self.board[
                row : row + strip_shape.shape[0],
                self.piece_x + shape_left : self.piece_x + shape.shape[1] - shape_right,
            ]
            print("Collision\n", collision_area)
            print("Shape\n", strip_shape)
            if (collision_area[np.nonzero(strip_shape)] == 0).all():
                self.board[
                    row : row + strip_shape.shape[0],
                    self.piece_x
                    + shape_left : self.piece_x
                    + shape.shape[1]
                    - shape_right,
                ] += strip_shape
                print(self.board)
                self.new_piece()
                print("DROPPED")
                break

    def step(self):
        pass
