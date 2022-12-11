#!/usr/bin/env python3
import os
import sys
from dataclasses import dataclass, field

####################### Helping functions###########################


@dataclass
class Machine:
    instructions: list = field(repr=False)
    clock: int = 0
    register_x: int = 1
    display_width: int = 40

    def pixel(self, clock_offset=-1):
        # We go one cycle back, since we already increased the counter
        o = (self.clock + clock_offset) % self.display_width
        return self.register_x in [o-1, o, o+1]

    def cycle(self):
        yield self
        for op, var in self.instructions:
            time = 1
            # Sleep
            match op:
                case "addx":
                    time = 2
                case "noop":
                    pass
            for _ in range(time):
                self.clock += 1
                yield self
            # Action
            match op:
                case "addx":
                    self.register_x += var
                case "noop":
                    pass


def draw_screen(machine):
    ret = ""
    for state in machine.cycle():
        # Do not print the initial clock state
        if state.clock == 0:
            continue
        if state.pixel():
            ret += "#"
        else:
            ret += "."
        if (state.clock) % state.display_width == 0:
            ret += "\n"
    return ret.removesuffix("\n")


def parse_text(screen):
    ret = ""
    lines = screen.split("\n")
    segment_length = 5

    for segment in range(0, len(lines[0]), segment_length):
        current_str = ""
        for j in range(len(lines)):
            for i in range(segment_length-1):
                current_str += lines[j][segment+i]
        # NOTE: This only works for some letters, specific to my output
        match current_str:
            case ".##.#..##..######..##..#":
                ret += "A"
            case "#####...###.#...#...####":
                ret += "E"
            case "#####...###.#...#...#...":
                ret += "F"
            case ".##.#..##...#.###..#.###":
                ret += "G"
            case "#...#...#...#...#...####":
                ret += "L"
            case "###.#..##..####.#...#...":
                ret += "P"
            case "#..##..##..##..##..#.##.":
                ret += "U"
            case default:
                # Blank if letter not found
                ret += " "
    return ret


def data_parser(filepath):
    """Parse the data by splitting each line."""
    with open(filepath, "r") as file:
        # split into lines
        ret = []
        for line in file.readlines():
            inst = line.removesuffix("\n").split(" ")
            if len(inst) == 1:
                ret.append((inst[0], None))
            else:
                ret.append((inst[0], int(inst[1])))

        return ret


######################### Main functions############################


def solver_1star(data):
    machine = Machine(data)
    clocks_of_internest = [x for x in range(20, 220 + 1, 40)]
    ret = 0
    for state in machine.cycle():
        if state.clock in clocks_of_internest:
            ret += state.clock * state.register_x
    return ret


def solver_2star(data):
    machine = Machine(data)
    ret = draw_screen(machine)
    return parse_text(ret)


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
