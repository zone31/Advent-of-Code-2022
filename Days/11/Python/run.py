#!/usr/bin/env python3
import os
import sys
from functools import partial
import math
import copy
####################### Helping functions###########################


def do_monkey_round(monkeys, common_value=None):
    for eid in range(len(monkeys)):
        monkey = monkeys[eid]
        # Iterate over items
        for _ in range(len(monkey["items"])):

            old_worry = monkey["items"].pop(0)
            new_worry = monkey["worry_func"](old_worry)

            if common_value is None:
                # Star 1
                new_worry = int(math.floor(new_worry/3))
            else:
                # Star 2
                if new_worry > common_value:
                    new_worry = new_worry - (math.floor(new_worry / common_value) * common_value)
            # Throw the stuff
            throw_to = monkey[monkey["test_func"](new_worry)]
            monkeys[throw_to]["items"].append(new_worry)

            # count that we touched the element
            monkey["inspected"] += 1


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, "r") as file:
        # split into Monkeys
        monkeys = [x for x in file.read().split("\n\n")]
        ret = {}
        for monkey in monkeys:
            elements = monkey.split("\n")
            mid = int(elements[0].split(" ")[1][:-1])
            ret[mid] = {}
            ret[mid]["inspected"] = 0
            ret[mid]["items"] = [int(x) for x in elements[1].split(":")[1].split(",")]
            ret[mid]["sign"] = elements[2].split("old ")[1][0]
            ret[mid]["const"] = elements[2].split("old ")[1][2:]

            def operator(sign, const, input):
                if const.isdigit():
                    const = int(const)
                else:
                    const = int(input)
                match sign:
                    case "+":
                        return const + input
                    case "*":
                        return const * input

            ret[mid]["worry_func"] = partial(operator, ret[mid]["sign"], ret[mid]["const"])
            ret[mid]["test_val"] = int(elements[3].split("by ")[1])
            ret[mid]["test_func"] = partial(lambda mod, input: not bool(input % mod), ret[mid]["test_val"])
            ret[mid][True] = int(elements[4].split("monkey ")[1])
            ret[mid][False] = int(elements[5].split("monkey ")[1])
    return ret


######################### Main functions############################


def solver_1star(data):
    data = copy.deepcopy(data)
    # Do 20 monkey rounds
    for _ in range(20):
        do_monkey_round(data)
    # Get the highest two inspected values
    tmp = sorted([x["inspected"] for x in data.values()], reverse=True)
    return tmp[0]*tmp[1]


def solver_2star(data):
    data = copy.deepcopy(data)
    # We observe in the dataset, that all branching conditions are prime
    # this means that we can calculate the total max value, before we can wrap
    # back around if we are over this common value
    common_value = math.prod([x["test_val"] for x in data.values()])
    # Do 10000 monkey rounds
    for _ in range(10000):
        do_monkey_round(data, common_value)
    # Get the highest two inspected values
    tmp = sorted([x["inspected"] for x in data.values()], reverse=True)
    return tmp[0]*tmp[1]


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
