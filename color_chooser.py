import math
import pyglet


class ColorChooser():
    def __init__(self, board, x, y):
        start_angle = 0
        angle = math.tau / len(board.paint_colors)
        self.sectors = []
        for color in board.paint_colors:
            self.sectors.append(pyglet.shapes.Sector(x, y,
                                                     radius=100,
                                                     angle=angle,
                                                     start_angle=start_angle,
                                                     color=color,
                                                     batch=board.batch))

            start_angle += angle
        board.color_chooser = self
