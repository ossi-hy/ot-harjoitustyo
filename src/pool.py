import random

class PiecePool:
    def __init__(self) -> None:
        self._refill()
        
    def _refill(self):
        self._pool = [i+1 for i in range(7)]
        random.shuffle(self._pool)

    def next_piece(self):
        if not self._pool:
            self._refill()
        return self._pool.pop()