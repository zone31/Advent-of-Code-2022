#!/usr/bin/env python3
import os
import sys
from enum import Enum, auto

####################### Helping functions###########################


def intersection(range1, range2):
    for (start1, stop1), (start2, stop2) in [[range1, range2], [range2, range1]]:
        if start1 <= start2 and stop1 >= stop2:
            return True
    return False


def count_overlap(range1, range2):
    set1 = set(range(range1[0], range1[1]+1))
    set2 = set(range(range2[0], range2[1]+1))
    return len(set1.intersection(set2)) > 0


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, 'r') as file:
        data = file.read()
        # Split up in segments
        sets = data.split("\n")
        ret = [[[int(z) for z in y.split("-")] for y in x.split(",")] for x in sets]
        return ret


######################### Main functions############################


def solver_1star(data):
    """
    We iterate over the elements, and find the intersection, if they fully intersect,
    we set that to true, and count the total
    """
    return sum([intersection(range1, range2) for range1, range2 in data])


def solver_2star(data):
    """
    Make the the ranges into sets, and compare their overlaps
    """
    return sum([count_overlap(range1, range2) for range1, range2 in data])


############################## MAIN#################################


def main(solve=0):
    """Run the program by itself, return a tuple of star1 and star2.

    solve: set what stars we want, 0 returns both
    """
    dirname = os.path.dirname(__file__)
    input_source = os.path.join(dirname, '..', 'input1.txt')
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
    day_path = os.path.normpath(os.path.join(file_path, '..'))
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
