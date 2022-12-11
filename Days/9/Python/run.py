#!/usr/bin/env python3
from enum import Flag, auto
import os
import sys

####################### Helping functions###########################


def follow_pos(head_pos, tail_pos):
    # if the pos is in the general area. do nothing
    delta = tuple(t-h for h, t in zip(head_pos, tail_pos))
    to_move = any([True for x in delta if abs(x) > 1])
    if to_move:
        clamp = tuple(max(-1, min(1, x)) for x in delta)
        return tuple(x-c for c, x in zip(clamp, tail_pos))
    else:
        return tail_pos


def pos_move(direction, pos, step=1):
    match direction:
        case "U":
            return (pos[0], pos[1]+step)
        case "D":
            return (pos[0], pos[1]-step)
        case "R":
            return (pos[0]+step, pos[1])
        case "L":
            return (pos[0]-step, pos[1])


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, "r") as file:
        # split into lines
        ret = []
        for line in file.readlines():
            direction, distance = line.removesuffix("\n").split(" ")
            ret.append((direction, int(distance)))

        return ret


######################### Main functions############################


def solver_1star(data):
    tail = (0, 0)
    head = (0, 0)
    tail_seen = set()
    tail_seen.add(tail)
    for direction, steps in data:
        for _ in range(steps):
            head = pos_move(direction, head)
            tail = follow_pos(head, tail)
            tail_seen.add(tail)
    return len(tail_seen)


def solver_2star(data):
    rope_length = 10
    tail_id = rope_length - 1
    rope = [(0, 0) for _ in range(rope_length)]
    tail_seen = set()
    tail_seen.add(rope[tail_id])
    for direction, steps in data:
        for _ in range(steps):
            # go over each link in the rope, and step them
            rope[0] = pos_move(direction, rope[0])
            for i in range(len(rope)-1):
                rope[i+1] = follow_pos(rope[i], rope[i+1])
            tail_seen.add(rope[tail_id])
    return len(tail_seen)

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
