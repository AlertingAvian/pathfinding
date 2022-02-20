# Copyright (c) 2022, Patrick Maloney
# All rights reserved.


import logging
import logging.config
from pathlib import Path
from random import random
from termcolor import colored
from dotenv import load_dotenv
from typing import List, Tuple
from dataclasses import dataclass
from os import system, name, environ


load_dotenv()
logging.config.fileConfig(Path(environ['LOGGING_CONFIG_PATH']))
dm_logger = logging.getLogger('displayMap')
dm_logger.debug('logger initialized')
mm_logger = logging.getLogger('makeMap')
mm_logger.debug('logger initialized')

###
# Make Map
###


@dataclass
class MapPoint:
    x: int
    y: int
    obstruction: bool = False
    start: bool = False
    end: bool = False


def create_array(x: int, y: int) -> List:
    mm_logger.debug(f'Creating array of size {x}x{y}')
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
            mm_logger.debug(f'Point at {x}, {y} is {point}')
    return(array)


def create_map(x: int, y: int, clear_chance: float = 0.75) -> List:
    mm_logger.debug(
        f'Creating map of size {x}x{y}, with clear chance of {clear_chance}')
    array = create_array(x, y)
    array = fill_map(array, clear_chance)
    return(array)

###
# Display Map
###


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
    start: Tuple[int, int] = None

    def __init__(self, array: List[List[MapPoint, ]]):
        self.map = self.__convert_mappoints_to_displaypoints(array)
        dm_logger.debug('MapDisplay initialized')

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
                        self.start = (x, y)
                        self.current_cell = (x, y)
                        display_array[x][y].start = True
                    case point if point.end:
                        display_array[x][y].end = True
                    case point if point.obstruction:
                        display_array[x][y].obstruction = True
                    case _:
                        pass
        return display_array

    def move(self, direction: str, array: List[List[DisplayPoint]] = None) -> CellInfo:
        """
        Moves the active cell to the next cell in the given direction.
        """
        if array is None:
            array = self.map
            dm_logger.debug('Array not provided. Using class variable map.')
        if not isinstance(array[0][0], DisplayPoint):
            dm_logger.error('Array is not a 2D array of DisplayPoints.')
            raise TypeError('Array is not a 2D array of DisplayPoints.')
        if direction == "up":
            new_cell = (self.current_cell[0] - 1, self.current_cell[1])
        elif direction == "down":
            new_cell = (self.current_cell[0] + 1, self.current_cell[1])
        elif direction == "left":
            new_cell = (self.current_cell[0], self.current_cell[1] - 1)
        elif direction == "right":
            new_cell = (self.current_cell[0], self.current_cell[1] + 1)
        else:
            dm_logger.error(
                f'Invalid move -> {direction}\nMust be one of: "up", "down", "left", "right"')
            raise ValueError(
                f'Invalid move -> {direction}\nMust be one of: "up", "down", "left", "right"')
        if new_cell[0] < 0 or new_cell[1] < 0 or new_cell[0] > len(array) - 1 or new_cell[1] > len(array[0]) - 1:
            dm_logger.error(f'Invalid move -> {direction}. Out of bounds.')
            raise ValueError(f'Invalid move -> {direction}. Out of bounds.')
        if array[new_cell[0]][new_cell[1]].obstruction:
            dm_logger.error(f'Invalid move -> {direction}. Obstructed.')
            raise ValueError(f'Invalid move -> {direction}. Obstructed.')
        self.last_cell = self.current_cell
        array[self.current_cell[0]][self.current_cell[1]].active = False
        self.current_cell = new_cell
        array[self.current_cell[0]][self.current_cell[1]].active = True
        array[self.current_cell[0]][self.current_cell[1]].searched = True
        return self.__get_cell_information(array, new_cell)

    def update_display(self, array: List[List[DisplayPoint]] = None):
        """
        Displays the map.
        """
        dm_logger.debug('Updating dispay.')
        if array is None:
            array = self.map
            dm_logger.debug('Array not provided. Using class variable map.')
        if not isinstance(array[0][0], DisplayPoint):
            dm_logger.error('Array is not a 2D array of DisplayPoints.')
            raise TypeError('Array is not a 2D array of DisplayPoints.')
        output_string = self.__display(array)
        self.__clear_terminal()
        print(output_string)

    def __clear_terminal(self) -> None:
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

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

    def __display(self, array: List[DisplayPoint]) -> str:
        active_color = 'blue'
        searched_color = 'magenta'
        x_len = len(array) + 2
        output_string = ''
        output_string += colored(' '*x_len, 'white', attrs=['reverse'])
        output_string += '\n'
        for x, row in enumerate(array):
            output_string += colored(' ', 'white', attrs=['reverse'])
            for y, point in enumerate(row):
                match point:
                    case point if point.start:
                        output_string += colored(' ',
                                                 'green', attrs=['reverse'])
                    case point if point.end:
                        output_string += colored(' ', 'red', attrs=['reverse'])
                    case point if point.obstruction:
                        output_string += colored(' ',
                                                 'white', attrs=['reverse'])
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
