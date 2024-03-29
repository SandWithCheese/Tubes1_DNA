from typing import Optional
from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from ..util import distance, get_diamond_button, get_direction, get_teleporters

RETREAT_DELAY: int = 0


class TargetDiamond:
    def __init__(self, position: Position, reward: int, distance: int, teleport: int):
        self.position = position  # Position of the diamond
        self.reward = reward  # Reward of the diamond
        self.distance = distance  # Distance from current position to diamond
        self.teleport = (
            teleport  # 0: without teleporter, 1: with teleporter1, 2: with teleporter2
        )


def get_target_diamonds(
    cur_pos: Position, t1: Position, t2: Position, diamonds: list[GameObject]
) -> list[TargetDiamond]:
    # Intialize all target diamonds possibility
    target_diamonds: list[TargetDiamond] = []

    # Fill list of all possible diamond position (without teleporter)
    for d in diamonds:
        new_diamond = TargetDiamond(
            d.position, d.properties.points, distance(d.position, cur_pos), 0
        )
        target_diamonds.append(new_diamond)

    # Fill the list of diamond position (with teleporter)
    for d in diamonds:
        # Get distance from current to teleporter
        dist_cur_to_t1 = distance(cur_pos, t1)
        dist_cur_to_t2 = distance(cur_pos, t2)

        # Get distance from teleporter to diamond
        dist_diamond_to_t1 = distance(d.position, t1)
        dist_diamond_to_t2 = distance(d.position, t2)

        # Get distance from current to diamond with teleporter
        dist_cur_to_diamond_with_t1 = dist_cur_to_t1 + dist_diamond_to_t1
        dist_cur_to_diamond_with_t2 = dist_cur_to_t2 + dist_diamond_to_t2

        # Append
        new_diamond_1 = TargetDiamond(
            d.position, d.properties.points, dist_cur_to_diamond_with_t1, 1
        )
        new_diamond_2 = TargetDiamond(
            d.position, d.properties.points, dist_cur_to_diamond_with_t2, 2
        )
        target_diamonds.append(new_diamond_1)
        target_diamonds.append(new_diamond_2)

    return target_diamonds


class TargetHome:
    def __init__(self, position: Position, distance: int, teleport: int):
        self.position = position  # Position of the home
        self.distance = distance  # Distance from current position to home
        self.teleport = (
            teleport  # 0: without teleporter, 1: with teleporter1, 2: with teleporter2
        )


def get_target_homes(
    cur_pos: Position, t1: Position, t2: Position, base: Position
) -> list[TargetHome]:
    # Initialize list of all possible home position (without teleporter)
    target_homes: list[TargetHome] = []

    # Fill the list of home position (without teleporter)
    new_home = TargetHome(base, distance(cur_pos, base), 0)
    target_homes.append(new_home)

    # Fill the list of home position (with teleporter)
    dist_cur_to_t1 = distance(cur_pos, t1)
    dist_cur_to_t2 = distance(cur_pos, t2)
    dist_base_to_t1 = distance(base, t1)
    dist_base_to_t2 = distance(base, t2)
    dist_cur_to_home_with_t1 = dist_cur_to_t1 + dist_base_to_t1
    dist_cur_to_home_with_t2 = dist_cur_to_t2 + dist_base_to_t2
    new_home_1 = TargetHome(t1, dist_cur_to_home_with_t1, 1)
    new_home_2 = TargetHome(t2, dist_cur_to_home_with_t2, 2)
    target_homes.append(new_home_1)
    target_homes.append(new_home_2)

    return target_homes


class DewoDTLogic(BaseLogic):
    # Constructor
    def __init__(self):
        pass

    # Prinsip Utama Greedy dewodt:
    # 1. Stoicism: Hindari sebsia mungkin hal-hal yang tidak bisa dikontrol/prediksi seperti tackle, red button.
    # 2. Efficient: Usahakan untuk kembali ke base jika hanya inventory full atau waktu tersisa kurang dari waktu yang dibutuhkan untuk kembali ke base.
    # 3. Diamond Button:
    # Jika dihitung bahwa jarak dari base ke diamond jauh (dibandingin oleh lawan kita), kita bisa saja menargetkan red button agar bisa dapat diamond yang lebih dekat.
    # Jika jumlah diamond <= 3 akan saling rebutan, maka target diamond button.
    # 4. Teleporter: Telep bisa dipakai untuk mengambil diamond yang jauh atau ke balik ke base jika jauh

    # Beberapa Strategi Greedy Pengambilan Reward:
    # 1. Ambil diamond dengan jarak terkecil
    # 2. Ambil diamond dengan reward terbesar
    # 3. Ambil diamond dengan reward/jarak terbesar
    # 4. Ambil diamond dengan jarak terdekat dari posisi sekarang namun tidak lebih dekat dari musuh ke diamond tersebut

    # Next move logic
    def next_move(self, board_bot: GameObject, board: Board):
        # Get position of our bot
        cur_pos = board_bot.position
        # Get base position of our base
        base = board_bot.properties.base
        # Get teleporters
        t1, t2 = get_teleporters(board.game_objects)
        # Get diamonds
        diamonds = board.diamonds
        # Get diamond button
        diamond_button: Optional[Position] = get_diamond_button(board.game_objects)
        # Initialize map of vunerable position (enemy position/adjacent position of enemy position)
        is_vulnerable = [[False for i in range(15)] for j in range(15)]

        # List of all possible diamond target path (with or without teleporter)
        target_diamonds = get_target_diamonds(cur_pos, t1, t2, diamonds)
        # List of all posible home target path (with or without teleporter)
        target_homes = get_target_homes(cur_pos, t1, t2, base)

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

        # Find closest diamond from current position
        closest_diamond = min(target_diamonds, key=lambda x: x.distance)

        # Find closest home from current position
        closest_home = min(target_homes, key=lambda x: x.distance)

        # Calculate distance to diamond button
        dist_cur_to_diamond_button = distance(cur_pos, diamond_button)

        # Get goal
        goal: Position

        # Conditions
        # All diamonds are taken
        isDiamondEmpty = len(diamonds) == 0

        # Inventory is full
        isCannotTakeMoreDiamond = (
            board_bot.properties.diamonds == board_bot.properties.inventory_size
            or (
                board_bot.properties.diamonds == board_bot.properties.inventory_size - 1
                and closest_diamond.reward == 2
            )
        )

        # Time not enough to get back to base
        isTimeNotEnough = (
            distance(cur_pos, closest_diamond.position)
            + distance(closest_diamond.position, closest_home.position)
            + RETREAT_DELAY
            > (board_bot.properties.milliseconds_left) / 1000.0
        )

        # Heuristic:
        # Jika jumlah diamond <= 3 dan jarak ke diamond lebih jauh dari orang lain akan saling rebutan, maka target diamond button.
        is_furthest_from_diamonds = True
        for enemy in board.bots:
            if enemy.id != board_bot.id:
                enemy_position = enemy.position
                enemy_target_diamonds = get_target_diamonds(
                    enemy_position, t1, t2, diamonds
                )
                enemy_closest_diamond = min(
                    enemy_target_diamonds, key=lambda x: x.distance
                )
                if closest_diamond.distance < enemy_closest_diamond.distance:
                    is_furthest_from_diamonds = False

        # Should our bot go to diamond button (reset)
        shouldGoToDiamondButton = len(diamonds) <= 3 and is_furthest_from_diamonds

        # Determine goal
        if isDiamondEmpty or isCannotTakeMoreDiamond or isTimeNotEnough:
            goal = base
        elif shouldGoToDiamondButton:
            goal = diamond_button
        else:
            if closest_diamond.teleport == 0:
                goal = closest_diamond.position
            elif closest_diamond.teleport == 1:
                goal = t1
            else:
                goal = t2

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
            return direction
        else:
            return (possibilities[0][0] - cur_pos.x, possibilities[0][1] - cur_pos.y)
