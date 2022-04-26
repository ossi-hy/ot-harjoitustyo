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
                np.zeros((self.gameboard.height, self.gameboard.width), np.uint8),
            )
        )

    def test_reset(self):
        self.gameboard.move(1)
        self.gameboard.rotate(1)
        self.gameboard.drop()
        self.gameboard.reset()

        self.assertTrue(
            np.array_equal(
                self.gameboard.board,
                np.zeros((self.gameboard.height, self.gameboard.width), np.uint8),
            )
        )
        self.assertEqual(self.gameboard.hold_id, -1)

    def test_clear_line(self):
        self.gameboard.board = np.zeros((self.gameboard.height, self.gameboard.width), np.uint8)
        self.gameboard.board[-1,:] = 1
        self.gameboard.clear_lines()
        self.assertTrue(
            np.array_equal(
                self.gameboard.board,
                np.zeros((self.gameboard.height, self.gameboard.width), np.uint8),
            )
        )

