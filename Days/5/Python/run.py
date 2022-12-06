#!/usr/bin/env python3
import os
import sys
from enum import Enum, auto
import copy

####################### Helping functions###########################


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, "r") as file:
        data = file.read()
        # Split the two segemtns
        top, bottom = [x.split("\n") for x in data.split("\n\n")]

        # parse smsegment 1 by lookng at the numbers in the bottom row
        spots = set(top[-1])
        spots.remove(" ")
        spots = sorted(spots)
        piles = {int(x): list() for x in spots}

        # Generate the piles
        for i in range(-2, -len(top) - 1, -1):
            for j in range(len(piles)):
                pile_id = j + 1
                data_offset = j * 4 + 1
                if top[i][data_offset] == " ":
                    continue
                piles[pile_id].append(top[i][data_offset])

        # Generate the instructions
        instructions = []
        for instruction in bottom:
            p_instruction = instruction.split(" ")
            instructions.append(
                {
                    "move": int(p_instruction[1]),
                    "from": int(p_instruction[3]),
                    "to": int(p_instruction[5]),
                }
            )

        return (piles, instructions)


######################### Main functions############################


def solver_1star(data):
    piles, instructions = data
    # Take a deep copy, so we do not rearrange data in star 2
    piles = copy.deepcopy(piles)
    for instruction in instructions:
        # Move the amount of times
        for _ in range(instruction["move"]):
            element = piles[instruction["from"]].pop()
            piles[instruction["to"]].append(element)

    # Generate the return
    ret = ""
    for pile in piles.values():
        ret += pile[-1]
    return ret


def solver_2star(data):
    piles, instructions = data
    # Take a deep copy, so we do not rearrange data in star 2
    piles = copy.deepcopy(piles)
    for instruction in instructions:
        # Move the amount of times
        stack = []
        for _ in range(instruction["move"]):
            stack.append(piles[instruction["from"]].pop())
        stack = reversed(stack)
        piles[instruction["to"]].extend(stack)

    # Generate the return
    ret = ""
    for pile in piles.values():
        ret += pile[-1]
    return ret


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
