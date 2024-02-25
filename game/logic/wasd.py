import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
import keyboard


class WASDLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def next_move(self, board_bot: GameObject, board: Board):
        key_pressed = keyboard.read_key()
        if key_pressed == 'w':
            delta_x, delta_y = self.directions[3]
        elif key_pressed == 's':
            delta_x, delta_y = self.directions[1]
        elif key_pressed == 'a':
            delta_x, delta_y = self.directions[2]
        elif key_pressed == 'd':
            delta_x, delta_y = self.directions[0]
        else:
            delta_x, delta_y = (0, 0)

        return delta_x, delta_y
