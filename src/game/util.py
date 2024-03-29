from .models import Position, GameObject
import random
from typing import Optional

direction_state = True


def distance(a: Position, b: Position):
    return abs(a.x - b.x) + abs(a.y - b.y)


def position_equals(a: Position, b: Position):
    return a.x == b.x and a.y == b.y


def get_direction(src: Position, dest: Position) -> set[tuple]:
    global direction_state
    direction_state = not direction_state
    is_right = dest.x > src.x
    is_bottom = dest.y > src.y

    if is_right:
        if is_bottom:
            if direction_state:
                return (1, 0)
            else:
                return (0, 1)
        else:
            if direction_state or src.y == dest.y:
                return (1, 0)
            else:
                return (0, -1)
    else:
        if is_bottom:
            if direction_state or src.x == dest.x:
                return (0, 1)
            else:
                return (-1, 0)
        else:
            if (src.y == dest.y or direction_state) and (src.x != dest.x):
                return (-1, 0)
            else:
                return (0, -1)


def get_teleporters(game_objects: list[GameObject]) -> list[Position]:
    teleporters = []
    for obj in game_objects:
        if obj.type == "TeleportGameObject":
            teleporters.append(obj.position)
    return teleporters


def get_diamond_button(game_objects: list[GameObject]) -> Optional[Position]:
    for obj in game_objects:
        if obj.type == "DiamondButtonGameObject":
            return obj.position
    return None


# def get_direction(src: Position, dest: Position):
#     is_right = dest.x > src.x
#     is_bottom = dest.y > src.y

#     rand = random.random()
#     if is_right:
#         if is_bottom:
#             if rand > 0.5:
#                 return (1, 0)
#             else:
#                 return (0, 1)
#         else:
#             if rand > 0.5 or src.y == dest.y:
#                 return (1, 0)
#             else:
#                 return (0, -1)
#     else:
#         if is_bottom:
#             if rand > 0.5 or src.x == dest.x:
#                 return (0, 1)
#             else:
#                 return (-1, 0)
#         else:
#             if (src.y == dest.y or rand > 0.5) and (src.x != dest.x):
#                 return (-1, 0)
#             else:
#                 return (0, -1)
