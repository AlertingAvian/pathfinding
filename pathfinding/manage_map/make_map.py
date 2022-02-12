# Copyright (c) 2022, Patrick Maloney
# All rights reserved.

from typing import List
from random import random
from termcolor import colored
from dataclasses import dataclass
from os import system, name


@dataclass
class MapPoint:
    x: int
    y: int
    obstruction: bool = False
    start: bool = False
    end: bool = False


def create_array(x: int, y: int) -> List:
    array = [[MapPoint(j, i) for i in range(y)] for j in range(x)]
    return array


def fill_map(array: List, clear_chance: float = 0.75) -> List:
    x_max = len(array) - 1
    y_max = len(array[0]) - 1
    for x, row in enumerate(array):
        for y, point in enumerate(row):
            match (x, y):
                case (0, 0):
                    point.start = True
                case (x, y) if (x, y) == (x_max, y_max):
                    point.end = True
                case _:
                    if round(random(), 2) > clear_chance:
                        point.obstruction = True
    return(array)


def create_static_display(array: List) -> str:
    x_len = len(array) + 2
    output_string = ''
    output_string += colored(' '*x_len, 'white', attrs=['reverse'])
    output_string += '\n'
    for x, row in enumerate(array):
        output_string += colored(' ', 'white', attrs=['reverse'])
        for y, point in enumerate(row):
            match point:
                case point if point.start:
                    output_string += colored(' ', 'green', attrs=['reverse'])
                case point if point.end:
                    output_string += colored(' ', 'red', attrs=['reverse'])
                case point if point.obstruction:
                    output_string += colored(' ', 'white', attrs=['reverse'])
                case _:
                    output_string += ' '
        output_string += colored(' ', 'white', attrs=['reverse'])
        output_string += '\n'
    output_string += colored(' '*x_len, 'white', attrs=['reverse'])
    return output_string


def create_map(x: int, y: int, clear_chance: float = 0.75) -> List:
    array = create_array(x, y)
    array = fill_map(array, clear_chance)
    return(array)


def clear_terminal() -> None:
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


if __name__ == "__main__":
    array = create_array(30, 30)
    map = fill_map(array, clear_chance=0.8)
    clear_terminal()
    print(create_static_display(map))
