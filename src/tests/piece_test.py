import unittest
import numpy as np
from piece import Piece

class PieceTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_rotated_line_piece(self):
        piece = Piece(6, 0, 0, -1)
        shape, _, _, _ = piece.get_shape()
        expected = np.array([[0,0,6,0],[0,0,6,0],[0,0,6,0],[0,0,6,0]])
        self.assertTrue(np.array_equal(expected, shape))
