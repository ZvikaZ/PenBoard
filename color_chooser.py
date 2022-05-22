import math
import pyglet


def contains(sector, x, y):
    angle = math.atan2(y - sector.y, x - sector.x)
    if angle < 0:
        angle += math.tau
    return math.dist([sector.x, sector.y], [x, y]) < sector.radius and \
           sector.start_angle <= angle <= sector.start_angle + sector.angle


class ColorChooser():
    def __init__(self, board, x, y):
        self.board = board
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

    def handle_click(self, x, y):
        sectors = [sector for sector in self.sectors if contains(sector, x, y)]
        if sectors:
            self.board.update_pen_color(sectors[0].color)

        self.board.color_chooser = None
