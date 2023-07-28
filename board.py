from chess_pieces import *
import numpy as np


class Board:
    def __init__(self) -> None:
        self.board = np.empty(shape=(8, 8), dtype=object)
        self.pawns = list()

    def initialize(self):
        for i in range(8):
            self.pawns.append(Pawn(6, i, "W"))
        for i in range(8):
            self.pawns.append(Pawn(1, i, "B"))
