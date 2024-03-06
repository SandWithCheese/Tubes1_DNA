from game.logic.base import BaseLogic
from game.models import GameObject, Board
from ..util import get_direction, distance


class ChaserLogic(BaseLogic):
    def __init__(self):
        pass

    def next_move(self, board_bot: GameObject, board: Board):
        if board_bot.properties.diamonds >= 3:
            return get_direction(board_bot, board_bot.properties.base)

        cur_pos = board_bot.position

        closest_enemy = None
        dist = 1024
        for enemy in board.bots:
            if (
                enemy.position != board_bot.position
                and "chaser" not in enemy.properties.name
            ):
                # self.enemy_history.append((enemy.position.x, enemy.position.y))
                enemy_dist = distance(cur_pos, enemy.position)
                if enemy_dist < dist:
                    dist = enemy_dist
                    closest_enemy = enemy
        if closest_enemy == None:
            if cur_pos.x == 0:
                return (1, 0)
            else:
                return (-1, 0)
        else:
            dir = get_direction(cur_pos, closest_enemy.position)
            return dir
