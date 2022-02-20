# Copyright (c) 2022, Patrick Maloney
# All rights reserved.

######################
# MOVED TO DISPLAY MAP
######################

import logging
import logging.config
from dotenv import load_dotenv
from pathlib import Path
from os import environ
from typing import List
from random import random
from dataclasses import dataclass

# load_dotenv()
# logging.config.fileConfig(Path(environ['LOGGING_CONFIG_PATH']))
# mm_logger = logging.getLogger('makeMap')
# mm_logger.debug('logger initialized')

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
    mm_logger.debug(f'Creating map of size {x}x{y}, with clear chance of {clear_chance}')
    array = create_array(x, y)
    array = fill_map(array, clear_chance)
    return(array)


if __name__ == "__main__":
    array = create_array(10, 10)
    map = fill_map(array, clear_chance=0.8)
    print(map)
