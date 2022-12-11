#!/usr/bin/env python3
from collections import OrderedDict
import os
import sys

####################### Helping functions###########################


def flatten_tree_and_get_sizes(tree, to_append=""):
    ret = {}
    # Get the root size
    if to_append == "":
        ret[f"folder|/"] = calculate_tree_size(tree)
    for key, value in tree.items():
        correct_key = f"{to_append}/{key}"
        if type(value) is dict:
            ret[f"folder|{correct_key}"] = calculate_tree_size(value)
            ret = ret | flatten_tree_and_get_sizes(value, correct_key)
        else:
            ret[f"file|{correct_key}"] = value
    return ret


def calculate_tree_size(tree):
    size = 0
    for value in tree.values():
        if type(value) is dict:
            size += calculate_tree_size(value)
        else:
            size += value
    return size


def generate_file_tree(commands: list[str]):
    """Iterate over the commands, and keep track of where we are by
    using a list of visited folders."""
    ret = {}
    path_stack = []
    for command in commands:
        if command.startswith("$"):
            command_segments = command.split(" ")
            if command_segments[1] == "cd":
                if command_segments[2] == "/":
                    path_stack = []
                elif command_segments[2] == "..":
                    path_stack.pop()
                else:
                    path_stack.append(command_segments[2])
        else:
            listing_segments = command.split(" ")
            tmp_ret = ret
            for dict_name in path_stack:
                tmp_ret = tmp_ret[dict_name]
            if listing_segments[0] == "dir":
                tmp_ret[listing_segments[1]] = {}
            else:
                tmp_ret[listing_segments[1]] = int(listing_segments[0])

    return ret


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, "r") as file:
        # split into lines
        return [x.removesuffix("\n") for x in file.readlines()]


######################### Main functions############################


def solver_1star(data):
    tree = generate_file_tree(data)
    flat_size = flatten_tree_and_get_sizes(tree)
    # Go over the fflat structure, and find all folders that is lower than
    # 100000, and som them together
    max_size = 100000
    ret = 0
    for path, size in flat_size.items():
        if path.startswith("folder") and size <= max_size:
            ret += size
    return ret


def solver_2star(data):
    tree = generate_file_tree(data)
    max_disk_size = 70000000
    needed_disk_size = 30000000
    minimum_disk_size = max_disk_size - needed_disk_size
    current_size = calculate_tree_size(tree)
    flat_size = flatten_tree_and_get_sizes(tree)
    folders = {
        key: value for key, value in flat_size.items() if key.startswith("folder")
    }
    sorted_folders = OrderedDict(sorted(folders.items(), key=lambda x: x[1]))
    for path, size in sorted_folders.items():
        # See what happens if we delete the folder
        new_size = current_size - size
        if new_size <= minimum_disk_size:
            return size


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
