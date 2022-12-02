#!/usr/bin/env python3
import os
import sys
from enum import Enum, auto

####################### Helping functions###########################


class Symbol(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


class Outcome(Enum):
    Loose = 0
    Draw = 3
    Win = 6


def duel_value(player: Symbol, opponent: Symbol):
    if player.value == opponent.value:
        return Outcome.Draw
    match (player, opponent):
        case (Symbol.Rock, Symbol.Paper):
            return Outcome.Loose
        case (Symbol.Rock, Symbol.Scissors):
            return Outcome.Win
        case (Symbol.Paper, Symbol.Rock):
            return Outcome.Win
        case (Symbol.Paper, Symbol.Scissors):
            return Outcome.Loose
        case (Symbol.Scissors, Symbol.Rock):
            return Outcome.Loose
        case (Symbol.Scissors, Symbol.Paper):
            return Outcome.Win


def letter_to_outcome(letter):
    match letter:
        case "X":
            return Outcome.Loose
        case "Y":
            return Outcome.Draw
        case "Z":
            return Outcome.Win


def letter_to_symbol(letter):
    match letter:
        case "A" | "X":
            return Symbol.Rock
        case "B" | "Y":
            return Symbol.Paper
        case "C" | "Z":
            return Symbol.Scissors


def data_parser(filepath):
    """Parse the data by splitting each line into a number."""
    with open(filepath, 'r') as file:
        data = file.read()
        # Split up in segments
        segments = data.split("\n")
        ret = [x.split(" ") for x in segments]
        return ret


######################### Main functions############################


def solver_1star(data):
    """
    We parse the element into enums for each player with a value of the points for that move,
    and calculate the win table.
    Then we sum all plays
    """
    ret = []
    for opponent, player in data:
        opponent = letter_to_symbol(opponent)
        player = letter_to_symbol(player)
        ret.append(duel_value(player, opponent).value + player.value)
    return sum(ret)


def solver_2star(data):
    """
    We detect what we should do, and calculate the winning move by adding, subtraction
    or keeping the opponents hand the same, and then wrapping it around with modulo
    """
    ret = []
    for opponent, play in data:
        opponent = letter_to_symbol(opponent)
        play = letter_to_outcome(play)
        match play:
            case Outcome.Win:
                player = Symbol((opponent.value - 1 + 1) % 3 + 1)
                ret.append(duel_value(player, opponent).value + player.value)
            case Outcome.Draw:
                player = Symbol((opponent.value - 1) % 3 + 1)
                ret.append(duel_value(player, opponent).value + player.value)
            case Outcome.Loose:
                player = Symbol((opponent.value - 1 - 1) % 3 + 1)
                ret.append(duel_value(player, opponent).value + player.value)
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
