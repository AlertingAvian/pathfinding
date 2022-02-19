# Copyright (c) 2022, Patrick Maloney
# All rights reserved.


from make_map import MapPoint

import logging
import logging.config
from dotenv import load_dotenv
from typing import List, Tuple
from os import system, name, environ
from pathlib import Path
from termcolor import colored
from dataclasses import dataclass


# TODO: finish move
# TODO: make functions default to class attribute map instead of having the array passed as a parameter
# TODO: setup logging
# TODO: provide way to inform search if exit is found -DONE


load_dotenv()
logging.config.fileConfig(Path(environ['LOGGING_CONFIG_PATH']))
logger = logging.getLogger('displayMap')
logger.debug('Logger initialized')


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


@dataclass
class CellInfo:
    """
    Class used to store information about a cell.
    is_exit - true if cell is an exit
    up, down, left, right: bool - True if the above cell is obstructed, None - if there is no cell above
    """
    is_exit: bool
    up: bool | None
    down: bool | None
    left: bool | None
    right: bool | None


class MapDisplay(object):
    current_cell: Tuple[int, int] = None
    last_cell: Tuple[int, int] = None

    def __init__(self, array: List[List[MapPoint, ]]):
        self.map = self.__convert_mappoints_to_displaypoints(array)

    def __convert_mappoints_to_displaypoints(self, array: List[List[MapPoint, ]]) -> List[List[DisplayPoint, ]]:
        """
        Converts a 2D array of MapPoints to a 2D array of DisplayPoints.
        """
        x_len = len(array)
        y_len = len(array[0])
        display_array = [[DisplayPoint(j, i)
                          for i in range(y_len)] for j in range(x_len)]
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

    def move(self, direction: str, array: List[List[DisplayPoint]] = [[None]]):
        """
        Moves the active cell to the next cell in the given direction.
        """
        if not isinstance(array[0][0], DisplayPoint):
            pass
        # if self.current_cell is not None:
        #     x, y = self.current_cell
        #     array[x][y].active = False
        #     self.last_cell = self.current_cell
        if direction == "up":
            new_cell = (self.current_cell[0] - 1, self.current_cell[1])
        elif direction == "down":
            new_cell = (self.current_cell[0] + 1, self.current_cell[1])
        elif direction == "left":
            new_cell = (self.current_cell[0], self.current_cell[1] - 1)
        elif direction == "right":
            new_cell = (self.current_cell[0], self.current_cell[1] + 1)
        else:
            raise ValueError(
                f'Invalid move -> {direction}\nMust be one of: "up", "down", "left", "right"')
        # NOT FINISHED

    def __get_cell_information(self, array: List[List[DisplayPoint]], coords: Tuple[int, int]) -> CellInfo:
        x, y = coords
        if x == 0:
            up = None
        else:
            up = array[x-1][y].obstruction
        if x == len(array) - 1:
            down = None
        else:
            down = array[x+1][y].obstruction
        if y == 0:
            left = None
        else:
            left = array[x][y-1].obstruction
        if y == len(array[0]) - 1:
            right = None
        else:
            right = array[x][y+1].obstruction
        is_exit = array[x][y].end
        return CellInfo(is_exit, up, down, left, right)


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
                            output_string += colored(' ',
                                                     active_color, attrs=['reverse'])
                        case point if point.searched:
                            output_string += colored(' ',
                                                     searched_color, attrs=['reverse'])
                        case _:
                            output_string += ' '
        output_string += colored(' ', 'white', attrs=['reverse'])
        output_string += '\n'
    output_string += colored(' '*x_len, 'white', attrs=['reverse'])
    return output_string


def update_display(array: List[List[DisplayPoint, ]]) -> None:
    """
    Updates the display of the map.
    """
    if not isinstance(array[0][0], DisplayPoint):
        raise TypeError('The array must be a 2D array of DisplayPoints.')
    output_string = __display(array)
    clear_terminal()
    print(output_string)


def clear_terminal() -> None:
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def get_cell_information(array: List[List[DisplayPoint]], coords: Tuple[int, int]) -> CellInfo:
    if not isinstance(array[0][0], DisplayPoint):
        raise TypeError('The array must be a 2D array of DisplayPoints.')
    x, y = coords
    if x == 0:
        up = None
    else:
        up = array[x-1][y].obstruction
    if x == len(array) - 1:
        down = None
    else:
        down = array[x+1][y].obstruction
    if y == 0:
        left = None
    else:
        left = array[x][y-1].obstruction
    if y == len(array[0]) - 1:
        right = None
    else:
        right = array[x][y+1].obstruction
    return CellInfo(up, down, left, right)
