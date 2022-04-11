import unittest
import random

from pool import PiecePool

class TestPiecePool(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(0)
        self.pool = PiecePool()

    def test_pieces_within_range(self):
        for _ in range(15):
            piece = self.pool.next_piece()
            self.assertGreaterEqual(piece, 1)
            self.assertLessEqual(piece, 7)

    def test_no_three_in_a_row(self):
        first = self.pool.next_piece()
        second = self.pool.next_piece()
        third = self.pool.next_piece()
        for _ in range(20):
            self.assertFalse(first == second and second == third)
            first = second
            second = third
            third = self.pool.next_piece()
