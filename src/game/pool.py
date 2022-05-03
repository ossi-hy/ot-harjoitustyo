from __future__ import annotations
import random
from typing import Optional


class PiecePool:
    def __init__(self, seed: Optional[int]) -> None:
        """Create pool object

        Args:
            seed (Optional[int]): seed for the random number generator
        """
        if seed is not None:
            random.seed(seed)
        self._refill()

    def _refill(self):
        """Private function used to refill the pool"""
        self._pool = [i + 1 for i in range(7)]
        random.shuffle(self._pool)

    def next_piece(self) -> int:
        """Get the next piece from the pool and refill if empty

        Returns:
            int: Id of the piece
        """
        if not self._pool:
            self._refill()
        return self._pool.pop()
