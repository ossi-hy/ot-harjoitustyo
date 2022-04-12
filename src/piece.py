import numpy as np

SHAPES = [
    np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]], dtype=np.uint8),
    np.array([[0, 2, 2], [2, 2, 0], [0, 0, 0]], dtype=np.uint8),
    np.array([[3, 3, 0], [0, 3, 3], [0, 0, 0]], dtype=np.uint8),
    np.array([[4, 0, 0], [4, 4, 4], [0, 0, 0]], dtype=np.uint8),
    np.array([[0, 0, 5], [5, 5, 5], [0, 0, 0]], dtype=np.uint8),
    np.array([[0, 0, 0, 0], [6, 6, 6, 6], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=np.uint8),
    np.array([[7, 7], [7, 7]], dtype=np.uint8),
]


class Piece:
    def __init__(self, piece_id: int, x: int, y: int, r: int) -> None:
        self.piece_id = piece_id
        self.x_pos = x
        self.y_pos = y
        self.rotation = r

    def get_shape(self) -> tuple[np.ndarray, int, int, int]:
        shape = SHAPES[self.piece_id - 1]
        shape = np.rot90(shape, self.rotation)
        shape_left = shape.any(0).argmax()
        shape_right = np.fliplr(shape).any(0).argmax()
        shape_bottom = np.flipud(shape).any(1).argmax()
        return shape, shape_left, shape_right, shape_bottom