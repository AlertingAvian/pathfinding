from typing import List
from random import getrandbits
from termcolor import colored


# DEBUG
import pprint
pp = pprint.PrettyPrinter(indent=4)


class MapPoint(object):
    up: bool = False
    down: bool = False
    left: bool = False
    right: bool = False

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


def create_array(x: int, y: int) -> List:
    array = [[MapPoint(j, i) for i in range(y)] for j in range(x)]
    return array


def fill_map(array: List) -> List: # not guaranteed solvable yet
    x_max = len(array) - 1
    y_max = len(array[0]) - 1
    for x, row in enumerate(array):
        row_upper = ''
        row_mid = ''
        row_lower = ''
        for y, point in enumerate(row):
            point.up = bool(getrandbits(1))
            point.down = bool(getrandbits(1))
            point.left = bool(getrandbits(1))
            point.right = bool(getrandbits(1))
            match (x, y):
                case (0, 0):
                    point.up = True
                    point.left = False
                case (0, y):
                    point.up = False
                case (x, 0):
                    point.left = False
                case (x_max, y_max):
                    point.right = False
                    point.down = True
                case (x_max, y):
                    point.down = False
                case (x, y_max):
                    point.right = False
                case _:
                    pass # ALREADY HANDLED
            wall = colored(" ", 'white', attrs=['reverse'])
            blank = " "
            block = f'{wall}{blank if point.up else wall}{wall}\n{blank if point.left else wall}{colored(" ", "red", attrs=["reverse"])}{blank if point.right else wall}\n{wall}{blank if point.down else wall}{wall}'
            lines = block.split('\n')
            row_upper += lines[0]
            row_mid += lines[1]
            row_lower += lines[2]
        print(f'{row_upper}\n{row_mid}\n{row_lower}')



def create_display(map: List) -> None:
    wall = colored("  ", 'white', attrs=['reverse'])
    blank = "  "
    # block = f'{wall}{blank if point.up else wall}{wall}\n{blank if point.left else wall}{blank}{blank if point.right else wall}\n{wall}{blank if point.down else wall}{wall}'



if __name__ == "__main__":
    array = create_array(10, 10)
    map = fill_map(array)
    # create_display(None)