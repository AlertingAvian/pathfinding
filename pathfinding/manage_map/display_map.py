# Copyright (c) 2022, Patrick Maloney
# All rights reserved.


from make_map import MapPoint


class DisplayPoint(MapPoint):
    """
    Subclass of MapPoint.
    Used to add additional functionality to MapPoint for display purposes.
    """

    def __init__(self, x: int, y: int, obstruction: bool = False, start: bool = False, end: bool = False):
        super().__init__(x, y, obstruction, start, end)

    def __str__(self):  # random ass shit made by copilot
        return super.__str__(self)

    def __reper__(self):
        return super.__repr__(self)
