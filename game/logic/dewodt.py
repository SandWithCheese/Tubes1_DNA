import random
from functools import cmp_to_key
from typing import Optional

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position

from ..util import distance, get_diamond_button, get_direction, get_teleporters

RETREAT_DELAY: int = 2


class DewoDTLogic(BaseLogic):
    # Constructor
    def __init__(self):
        pass

    # Prinsip Utama Greedy dewodt:
    # 1. Stoicism: Hindari sebsia mungkin hal-hal yang tidak bisa dikontrol/prediksi seperti tackle, red button.
    # 2. Efficient: Usahakan untuk kembali ke base jika hanya inventory full atau waktu tersisa kurang dari waktu yang dibutuhkan untuk kembali ke base.
    # 3. Bad Privilage: Jika dihitung bahwa jarak dari base ke diamond jauh (dibandingin oleh lawan kita), kita bisa saja menargetkan red button agar bisa dapat diamond yang lebih dekat.

    # Beberapa Strategi Greedy Pengambilan Reward:
    # 1. Ambil diamond dengan jarak terkecil
    # 2. Ambil diamond dengan reward terbesar
    # 3. Ambil diamond dengan reward/jarak terbesar
    # 4. Ambil diamond dengan jarak terdekat dari posisi sekarang namun tidak lebih dekat dari musuh ke diamond tersebut

    # Next move logic
    def next_move(self, board_bot: GameObject, board: Board):
        # Get position of our bot
        cur_pos = board_bot.position
        # Get base position of our bot
        base = board_bot.properties.base
        # Get teleporters
        t1, t2 = get_teleporters(board.game_objects)
        # Get diamond button
        diamond_button: Optional[Position] = get_diamond_button(board.game_objects)

        # Initialize map of red diamonds (2 points)
        is_red = [[False for i in range(15)] for j in range(15)]
        # Initialize map of vunerable position (enemy position/adjacent position of enemy position)
        is_vulnerable = [[False for i in range(15)] for j in range(15)]
        # Initialize list of diamond position (sorted by some criteria)
        diamonds: list[Position] = []

        # Fill the map of red diamonds & list of diamond position (without teleporter)
        for d in board.diamonds:
            diamonds.append(d.position)
            if d.properties.points == 2:
                is_red[d.position.x][d.position.y] = True

        # Fungsi seleksi memilih node terbaik berdasarkan JARAK TERDEKAT
        # Diamond dengan jarak terdekat (baik dengan teleporter maupun tidak)
        def selectionFunction() -> Position:
            # Find closest distance diamond from current position (without teleporter)
            pos_cur_to_closest_diamond_without_teleporter = min(
                diamonds, key=lambda x: distance(x, cur_pos)
            )
            dist_cur_to_diamond_without_teleporter = distance(
                pos_cur_to_closest_diamond_without_teleporter, cur_pos
            )

            # Find closest distance from current to t1 to diamond (with teleporter)
            dist_cur_to_t1 = distance(cur_pos, t1)
            pos_closest_diamond_to_t1 = min(diamonds, key=lambda x: distance(x, t1))
            dist_closest_diamond_to_t1 = distance(pos_closest_diamond_to_t1, t1)
            dist_closest_diamond_to_cur_with_t1 = (
                dist_cur_to_t1 + dist_closest_diamond_to_t1
            )

            # Find closest distance from current to t2 to diamond (with teleporter)
            dist_cur_to_t2 = distance(cur_pos, t2)
            pos_closest_diamond_to_t2 = min(diamonds, key=lambda x: distance(x, t2))
            dist_closest_diamond_to_t2 = distance(pos_closest_diamond_to_t2, t2)
            dist_closest_diamond_to_cur_with_t2 = (
                dist_cur_to_t2 + dist_closest_diamond_to_t2
            )

            # Diamond button is used when

            if (
                dist_cur_to_diamond_without_teleporter
                >= dist_closest_diamond_to_cur_with_t1
                and dist_cur_to_diamond_without_teleporter
                >= dist_closest_diamond_to_cur_with_t2
            ):
                # Langsung ke diamond (tanpa teleporter)
                return pos_cur_to_closest_diamond_without_teleporter
            elif (
                dist_closest_diamond_to_cur_with_t1
                >= dist_cur_to_diamond_without_teleporter
                and dist_closest_diamond_to_cur_with_t1
                >= dist_closest_diamond_to_cur_with_t2
            ):
                # Ke t1 dulu
                return t1
            else:
                # Ke t2 dulu
                return t2

        # Fill the map of vunerable position
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

        # Get goal
        goal: Position

        # Conditions
        target_diamond_or_button = selectionFunction()
        isDiamondEmpty = len(diamonds) == 0
        isCannotTakeMoreDiamond = (
            board_bot.properties.diamonds == board_bot.properties.inventory_size
            or (
                board_bot.properties.diamonds == board_bot.properties.inventory_size - 1
                and is_red[target_diamond_or_button.x][target_diamond_or_button.y]
            )
        )
        isTimeNotEnough = (
            distance(cur_pos, target_diamond_or_button)
            + distance(target_diamond_or_button, base)
            + RETREAT_DELAY
            > (board_bot.properties.milliseconds_left) / 1000.0
        )

        # Determine goal
        if isDiamondEmpty or isCannotTakeMoreDiamond or isTimeNotEnough:
            goal = base
        else:
            goal = target_diamond_or_button

        # Calculate possible moves
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

        # Return the move
        if (
            (cur_pos.x + direction[0], cur_pos.y + direction[1]) in possibilities
        ) or not len(possibilities):
            # self.history.append((cur_pos.x + direction[0], cur_pos.y + direction[1]))
            return direction
        else:
            # self.history.append((possibilities[0][0], possibilities[0][1]))
            return (possibilities[0][0] - cur_pos.x, possibilities[0][1] - cur_pos.y)
