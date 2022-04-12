import random
from typing import Optional


class PiecePool:
    def __init__(self, seed: Optional[int]) -> None:
        if seed:
            random.seed(seed)
        self._refill()

    def _refill(self):
        self._pool = [i + 1 for i in range(7)]
        random.shuffle(self._pool)

    def next_piece(self) -> int:
        if not self._pool:
            self._refill()
        return self._pool.pop()
