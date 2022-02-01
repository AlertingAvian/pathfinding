from typing import List


# DEBUG
import pprint
pp = pprint.PrettyPrinter(indent=4)


def create_array(x: int, y: int) -> List:
    array = [[{'up': False, 'down': False, 'left': False, 'right': False} for i in range(y)] for j in range(x)]
    return array


def fill_map(array: List) -> List:
    for z, z_val in enumerate(array):
        for x, x_val in enumerate(z_val):
            for y, y_val in enumerate(x_val):
                print(x, y)
                print(x_val, y_val)


if __name__ == "__main__":
    array = create_array(10, 10)
    map = fill_map(array)
