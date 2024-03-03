import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, distance
from functools import cmp_to_key

import time

RETREAT_DELAY: int = 2


# Density calculation
DENSITY_SIDE: int = 5
DENSITY_WEIGHT: float = 3
DISTANCE_WEIGHT: float = 1

class GreedyDense(BaseLogic):

    def __init__(self):
        pass

    def next_move(self, board_bot: GameObject, board: Board):
        cur_pos = board_bot.position
        base = board_bot.properties.base
        is_red = [[False for i in range(15)] for j in range(15)]
        is_diamond = [[False for i in range(15)] for j in range(15)]
        is_vulnerable = [[False for i in range(15)] for j in range(15)]
        diamonds: list[Position] = []

        for d in board.diamonds:
            diamonds.append(d.position)
            is_diamond[d.position.x][d.position.y] = True
            if d.properties.points == 2:
                is_red[d.position.x][d.position.y] = True
        def compare_distance(first_pos: Position, second_pos: Position):
            first_density, second_density = 0, 0
            for dx in range(-(DENSITY_SIDE // 2), (DENSITY_SIDE // 2) + 1):
                for dy in range(-(DENSITY_SIDE // 2), (DENSITY_SIDE // 2) + 1):
                    if 0 <= first_pos.x + dx < 15 and 0 <= first_pos.y + dy < 15 and is_diamond[first_pos.x + dx][first_pos.y + dy]:
                        first_density += 1
                        if is_red[first_pos.x][first_pos.y]:
                            first_density += 1
            first_density /= (DENSITY_SIDE ** 2)

            for dx in range(-(DENSITY_SIDE // 2), (DENSITY_SIDE // 2) + 1):
                for dy in range(-(DENSITY_SIDE // 2), (DENSITY_SIDE // 2) + 1):
                    if 0 <= second_pos.x + dx < 15 and 0 <= second_pos.y + dy < 15 and is_diamond[second_pos.x + dx][second_pos.y + dy]:
                        second_density += 1
                        if is_red[second_pos.x][second_pos.y]:
                            first_density += 1
            second_density /= (DENSITY_SIDE ** 2)

            first_value = first_density * DENSITY_WEIGHT + distance(first_pos, cur_pos) * DISTANCE_WEIGHT
            second_value = second_density * DENSITY_WEIGHT + distance(second_pos, cur_pos) * DISTANCE_WEIGHT
            return first_value - second_value
        

        diamonds.sort(key=cmp_to_key(compare_distance))

        for enemy in board.bots:
            if enemy.id != board_bot.id:
                enemy_pos = enemy.position
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if (dx == 0 or dy == 0) and 0 <= enemy_pos.x + dx < 15 and 0 <= enemy_pos.y + dy < 15:
                            is_vulnerable[enemy_pos.x + dx][enemy_pos.y + dy] = True
        for teleport in board.game_objects:
            if teleport.type == "TeleportGameObject":
                is_vulnerable[teleport.position.x][teleport.position.y] = True
                # for dx in [-1, 0, 1]:
                #     for dy in [-1, 0, 1]:
                #         if ((dx == 0) ^ (dy == 0)) and 0 <= teleport.position.x + dx < 15 and 0 <= teleport.position.y + dy < 15: 
                #             is_vulnerable[teleport.position.x + dx][teleport.position.y + dy] = True

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
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if ((dx == 0) ^ (dy == 0)) and 0 <= cur_pos.x + dx < 15 and 0 <= cur_pos.y + dy < 15 and not is_vulnerable[cur_pos.x + dx][cur_pos.y + dy]:
                    possibilities.append((dx, dy))
        if direction in possibilities or len(possibilities) == 0:
            return direction
        else:
            return possibilities[0]