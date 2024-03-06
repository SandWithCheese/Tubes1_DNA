import random
from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, get_teleporters, get_diamond_button, distance
from functools import cmp_to_key

RETREAT_DELAY: int = 2


class SandwichLogic(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.preference = ["button", "teleporter"]

    def next_move(self, board_bot: GameObject, board: Board):
        t1, t2 = get_teleporters(board.game_objects)
        diamond_button: Optional[Position] = get_diamond_button(board.game_objects)

        cur_pos = board_bot.position
        base = board_bot.properties.base

        is_red = [[False for i in range(15)] for j in range(15)]
        diamonds: list[Position] = []

        for d in board.diamonds:
            diamonds.append(d.position)
            if d.properties.points == 2:
                is_red[d.position.x][d.position.y] = True

        def compare_distance(first_pos: Position, second_pos: Position):
            return distance(first_pos, cur_pos) - distance(second_pos, cur_pos)

        diamonds.sort(key=cmp_to_key(compare_distance))

        closest_diamond_to_t1 = min(diamonds, key=lambda x: distance(x, t1))
        closest_diamond_distance_to_t1 = compare_distance(closest_diamond_to_t1, t1)

        closest_diamond_to_t2 = min(diamonds, key=lambda x: distance(x, t2))
        closest_diamond_distance_to_t2 = compare_distance(closest_diamond_to_t2, t2)

        is_vulnerable = [[False for i in range(15)] for j in range(15)]
        for enemy in board.bots:
            if enemy.id != board_bot.id:
                enemy_pos = enemy.position
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
        if (
            len(diamonds) == 0
            or board_bot.properties.diamonds == board_bot.properties.inventory_size
            or distance(cur_pos, diamonds[0])
            + distance(diamonds[0], base)
            + RETREAT_DELAY
            > (board_bot.properties.milliseconds_left) / 1000.0
            or (
                board_bot.properties.diamonds == board_bot.properties.inventory_size - 1
                and is_red[diamonds[0].x][diamonds[0].y]
            )
        ):
            if abs(compare_distance(cur_pos, t1)) + abs(
                compare_distance(t1, base)
            ) < abs(compare_distance(cur_pos, base)):
                goal = t1
            elif abs(compare_distance(cur_pos, t2)) + abs(
                compare_distance(t2, base)
            ) < abs(compare_distance(cur_pos, base)):
                goal = t2
            else:
                goal = base
        else:
            preference = random.choice(self.preference)
            if preference == "button":
                if compare_distance(diamond_button, cur_pos) < compare_distance(
                    diamonds[0], cur_pos
                ):
                    goal = diamond_button
                else:
                    goal = diamonds[0]
            else:
                if compare_distance(t1, cur_pos) < compare_distance(t2, cur_pos):
                    if (
                        compare_distance(t1, cur_pos) + closest_diamond_distance_to_t1
                    ) < compare_distance(diamonds[0], cur_pos):
                        goal = t1
                    else:
                        goal = diamonds[0]
                else:
                    if (
                        compare_distance(t2, cur_pos) + closest_diamond_distance_to_t2
                    ) < compare_distance(diamonds[0], cur_pos):
                        goal = t2
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

        if (
            (cur_pos.x + direction[0], cur_pos.y + direction[1]) in possibilities
        ) or not len(possibilities):
            return direction
        else:
            return (possibilities[0][0] - cur_pos.x, possibilities[0][1] - cur_pos.y)
