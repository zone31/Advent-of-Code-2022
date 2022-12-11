#!/usr/bin/env python3
from enum import Flag, auto
import os
import sys

####################### Helping functions###########################


class BlockedFrom(Flag):
    FREE = 0
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()
    ALL = TOP+BOTTOM+LEFT+RIGHT


def blocked_from(forrest, position: tuple[int, int]):
    x, y = position
    height, width = forrest_dimensions(forrest)
    visible_from = BlockedFrom.FREE
    # Iterate over each side
    tree = get_tree(forrest, position)
    for i in range(height):
        other = get_tree(forrest, (x, i))
        if other >= tree and i != y:
            if i > y:
                visible_from = visible_from | BlockedFrom.BOTTOM
            else:
                visible_from = visible_from | BlockedFrom.TOP

    for j in range(width):
        other = get_tree(forrest, (j, y))
        if other >= tree and j != x:
            if j > x:
                visible_from = visible_from | BlockedFrom.RIGHT
            else:
                visible_from = visible_from | BlockedFrom.LEFT
    return visible_from


def scenic_score(forrest, position: tuple[int, int]):
    x, y = position
    height, width = forrest_dimensions(forrest)
    tree = get_tree(forrest, position)
    ret = 1
    # Iterate over the directions
    iterations = [
        {"start": y-1, "stop": -1,     "step": -1, "pos": lambda x, y, l: (x, l)},
        {"start": y+1, "stop": height, "step": 1,  "pos": lambda x, y, l: (x, l)},
        {"start": x-1, "stop": -1,     "step": -1, "pos": lambda x, y, l: (l, y)},
        {"start": x+1, "stop": width,  "step": 1,  "pos": lambda x, y, l: (l, y)},
    ]

    for iteration in iterations:
        accum = 0
        for l in range(iteration["start"], iteration["stop"], iteration["step"]):
            other = get_tree(forrest, iteration["pos"](x, y, l))
            if tree > other:
                accum += 1
            else:
                accum += 1
                break
        ret = ret * accum
    return ret


def forrest_dimensions(forrest):
    return (len(forrest), len(forrest[0]))


def get_tree(forrest, position):
    x, y = position
    return forrest[y][x]


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, "r") as file:
        # split into lines
        return [[int(y) for y in x.removesuffix("\n")] for x in file.readlines()]


######################### Main functions############################


def solver_1star(data):
    height, width = forrest_dimensions(data)
    # Test all trees, and count the ones that are fully blocked
    fully_blocked = 0
    for x in range(width):
        for y in range(height):
            if (blocked_from(data, (x, y)) & BlockedFrom.ALL) == BlockedFrom.ALL:
                fully_blocked += 1

    return height*width - fully_blocked


def solver_2star(data):
    height, width = forrest_dimensions(data)
    # Test all trees, and get the max scenic score
    ret = []
    for x in range(width):
        for y in range(height):
            ret.append(scenic_score(data, (x, y)))
    return max(ret)

############################## MAIN#################################


def main(solve=0):
    """Run the program by itself, return a tuple of star1 and star2.

    solve: set what stars we want, 0 returns both
    """
    dirname = os.path.dirname(__file__)
    input_source = os.path.join(dirname, "..", "input1.txt")
    # Make list, since the generator has to be used multiple times
    data = data_parser(input_source)
    match solve:
        case 0:
            return (solver_1star(data), solver_2star(data))
        case 1:
            return (solver_1star(data), None)
        case 2:
            return (None, solver_2star(data))
        case _:
            raise Exception(f"solve set wrong! ({solve})")


def day_name():
    """Get the date name from the folder."""
    file_path = os.path.dirname(__file__)
    day_path = os.path.normpath(os.path.join(file_path, ".."))
    return os.path.basename(day_path)


if __name__ == "__main__":
    solve = 0
    if len(sys.argv) == 2:
        solve = int(sys.argv[1])
    star1, star2 = main(solve)

    match solve:
        case 0:
            day = day_name()
            print(f"Day {day} first star:")
            print(star1)
            print(f"Day {day} second star:")
            print(star2)
        case 1:
            print(star1)
        case 2:
            print(star2)
        case _:
            raise Exception(f"solve set wrong! ({solve})")
