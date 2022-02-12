# Copyright (c) 2022, Patrick Maloney
# All rights reserved.


from pathfinding.manage_map.make_map import MapPoint


class DisplayPoint(MapPoint):
    """
    Subclass of MapPoint.
    Used to add additional functionality to MapPoint for display purposes.
    """
    def __init__(self, x: int, y: int, obstruction: bool = False, start: bool = False, end: bool = False):
        super().__init__(x, y, obstruction, start, end)

    def __str__(self):
        match self.obstruction:
            case True:
                return 'X'
            case False:
                match self.start:
                    case True:
                        return 'S'
                    case False:
                        match self.end:
                            case True:
                                return 'E'
                            case False:
                                return ' '

test = DisplayPoint(1, 1)
print(test)