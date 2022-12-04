#!/usr/bin/env python3
import os
import sys
from enum import Enum, auto

####################### Helping functions###########################


def letter_to_value(letter: str):
    value = ord(letter.lower())-ord('a') + 1
    if letter.isupper():
        value += 26
    return value


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, 'r') as file:
        data = file.read()
        # Split up in segments
        return data.split("\n")


######################### Main functions############################


def solver_1star(data):
    """
    Go over each rucksack, and split them in two, use set intersection
    to find the same element in each. Then convert to number.
    """
    ret = []
    for rucksack in data:
        # split string, and convert to sets
        part1 = set(rucksack[:len(rucksack)//2])
        part2 = set(rucksack[len(rucksack)//2:])

        # Find the intersection between the sets, and convert the value
        same_elements = part1.intersection(part2)
        ret.append(letter_to_value(same_elements.pop()))

    return sum(ret)


def solver_2star(data):
    ret = []
    for rucksack1, rucksack2, rucksack3 in zip(*[iter(data)]*3):
        part1 = set(rucksack1)
        part2 = set(rucksack2)
        part3 = set(rucksack3)
        tmp = part1.intersection(part2)
        same_elements = tmp.intersection(part3)
        ret.append(letter_to_value(same_elements.pop()))

    return sum(ret)

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
