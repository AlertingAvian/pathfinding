# Copyright (c) 2022, Patrick Maloney
# All rights reserved.


from make_map import MapPoint

from typing import List
from os import system, name
from termcolor import colored


class DisplayPoint(MapPoint):
    """
    Subclass of MapPoint.
    Used to add additional functionality to MapPoint for display purposes.
    """

    def __init__(self, x: int, y: int, obstruction: bool = False, start: bool = False, end: bool = False):
        super().__init__(x, y, obstruction, start, end)
        self.active = False
        self.searched = False

    def __str__(self):  # random ass shit made by copilot
        return super.__str__(self)

    def __reper__(self):
        return super.__repr__(self)


def __display(array: List[DisplayPoint]) -> str:
    active_color = 'yellow'
    searched_color = 'grey'
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
                    match point:
                        case point if point.active:
                            output_string += colored(' ', active_color, attrs=['reverse'])
                        case point if point.searched:
                            output_string += colored(' ', searched_color, attrs=['reverse'])
                        case _:
                            output_string += ' '
        output_string += colored(' ', 'white', attrs=['reverse'])
        output_string += '\n'
    output_string += colored(' '*x_len, 'white', attrs=['reverse'])
    return output_string


def convert_mappoints_to_displaypoints(array: List[MapPoint]) -> List[DisplayPoint]:
    """
    Converts a 2D array of MapPoints to a 2D array of DisplayPoints.
    """
    x_len = len(array)
    y_len = len(array[0])
    display_array = [[DisplayPoint(j, i) for i in range(y_len)] for j in range(x_len)]
    for x, row in enumerate(array):
        for y, point in enumerate(row):
            match point:
                case point if point.start:
                    display_array[x][y].start = True
                case point if point.end:
                    display_array[x][y].end = True
                case point if point.obstruction:
                    display_array[x][y].obstruction = True
                case _:
                    pass
    return display_array


def update_display(array: List[DisplayPoint]) -> None:
    """
    Updates the display of the map.
    """
    output_string = __display(array)
    clear_terminal()
    print(output_string)


def clear_terminal() -> None:
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
