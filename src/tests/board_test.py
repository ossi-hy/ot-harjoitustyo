import unittest
import numpy as np
from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.gameboard = Board()

    def test_empty_board(self):
        self.assertTrue(
            np.array_equal(
                self.gameboard.board,
                np.zeros((self.gameboard.h, self.gameboard.w), np.uint8),
            )
        )
