import numpy as np

class Board:
    def __init__(self, width=10, height=20):
        self.w = width # pylint: disable=invalid-name
        self.h = height # pylint: disable=invalid-name
        self.board = np.zeros((self.h,self.w), dtype=np.uint8)
