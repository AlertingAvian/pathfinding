# Copyright (c) 2022, Patrick Maloney
# All rights reserved.


import PySimpleGUI as sg
from make_map import MapPoint

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


class Window(object):
    """
    Class for managing the window.
    """

    def __init__(self, map_width: int, map_height: int, title: str, cell_size: int = 40, padding: int = 40):
        self.map_width = map_width
        self.map_height = map_height
        self.width = map_width * 10 + (padding * 2)
        self.height = map_height * 10 + (padding * 2)
        self.window_size = (self.width, self.height)
        self.title = title
        self.theme = sg.theme('Topanga')

        self.layout = [[sg.Canvas(size=(self.map_height*cell_size, self.map_width*cell_size), background_color='black', key='canvas')],
                       [sg.Button('Start', key='start'), sg.Button('Stop', key='stop', disabled=True), sg.Button('Reset', key='reset'), sg.Button('Quit', key='quit', button_color=('white', 'red'))]]
        
        self.window = sg.Window(self.title, layout=self.layout)
        self.canvas = self.window['canvas'].TKCanvas
        self.canvas.TKCanvas.itemconfig(self.canvas.TKCanvas.create_polygon(0, 0, cell_size, cell_size, bg='white'))
        self.window.finalize()

test_window = Window(10, 10, 'Test Window')
input('Press enter to continue...')

