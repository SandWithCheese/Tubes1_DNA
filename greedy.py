import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, distance
from functools import cmp_to_key

RETREAT_DELAY: int = 2

class GreedyLogic(BaseLogic):

    def __init__(self):
        pass
        # self.count = 0
        # self.history: list[Position] = []
        # self.enemy_history: list[Position] = []

    def next_move(self, board_bot: GameObject, board: Board):
        # self.count += 1
        cur_pos = board_bot.position
        base = board_bot.properties.base
        is_red = [[False for i in range(15)] for j in range(15)]
        is_vulnerable = [[False for i in range(15)] for j in range(15)]
        diamonds: list[Position] = []

        for d in board.diamonds:
            diamonds.append(d.position)
            if d.properties.points == 2:
                is_red[d.position.x][d.position.y] = True
        def compare_distance(first_pos: Position, second_pos: Position):
            return distance(first_pos, cur_pos) - distance(second_pos, cur_pos)
        diamonds.sort(key=cmp_to_key(compare_distance))

        for enemy in board.bots:
            if enemy.id != board_bot.id:
                enemy_pos = enemy.position
                # self.enemy_history.append((enemy_pos.x, enemy_pos.y))
                is_vulnerable[enemy_pos.x][enemy_pos.y] = True
                if enemy_pos.x + 1 < 15:
                    is_vulnerable[enemy_pos.x + 1][enemy_pos.y] = True
                if enemy_pos.x - 1 >= 0:
                    is_vulnerable[enemy_pos.x - 1][enemy_pos.y] = True
                if enemy_pos.y + 1 < 15:
                    is_vulnerable[enemy_pos.x][enemy_pos.y + 1] = True
                if enemy_pos.y - 1 >= 0:
                    is_vulnerable[enemy_pos.x][enemy_pos.y - 1] = True
        
        goal: Position
        if     (len(diamonds) == 0
                or board_bot.properties.diamonds == board_bot.properties.inventory_size
                or distance(cur_pos, diamonds[0]) + distance(diamonds[0], base) + RETREAT_DELAY > (board_bot.properties.milliseconds_left) / 1000.0
                or (board_bot.properties.diamonds == board_bot.properties.inventory_size - 1 and is_red[diamonds[0].x][diamonds[0].y])):
            goal = base
        else:
            goal = diamonds[0]

        direction = get_direction(cur_pos, goal)
        possibilities: list[tuple] = []
        if cur_pos.x + 1 < 15 and not is_vulnerable[cur_pos.x + 1][cur_pos.y]:
            possibilities.append((cur_pos.x + 1, cur_pos.y))

        if cur_pos.y + 1 < 15 and not is_vulnerable[cur_pos.x][cur_pos.y + 1]:
            possibilities.append((cur_pos.x, cur_pos.y + 1))
        
        if cur_pos.x - 1 >= 0 and not is_vulnerable[cur_pos.x - 1][cur_pos.y]:
            possibilities.append((cur_pos.x - 1, cur_pos.y))
        
        if cur_pos.y - 1 >= 0 and not is_vulnerable[cur_pos.x][cur_pos.y - 1]:
            possibilities.append((cur_pos.x, cur_pos.y - 1))
        
        if ((cur_pos.x + direction[0], cur_pos.y + direction[1]) in possibilities) or not len(possibilities):
            # self.history.append((cur_pos.x + direction[0], cur_pos.y + direction[1]))
            return direction
        else:
            # self.history.append((possibilities[0][0], possibilities[0][1]))
            return (possibilities[0][0] - cur_pos.x, possibilities[0][1] - cur_pos.y)
    