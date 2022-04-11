import numpy as np

class Board:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = np.zeros((self.height,self.width), dtype=np.uint8)
