import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

directions = [(2, 0), (0, 1), (-1, 0), (0, -1)]

class CircularLogic(BaseLogic):
    def __init__(self):
        self.previous = 0

    def next_move(self, board_bot: GameObject, board: Board):
        self.previous += 1
        self.previous %= 4
        return directions[self.previous]