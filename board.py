import math
import pyglet
from misc import get_max_screens_width, get_max_screens_height

BACKGROUND_COLOR = (1.0, 1.0, 1.0, 1.0)
GRID_COLOR = (200, 200, 200)
GRID_WIDTH = 60
PAINT_COLORS = [(0, 0, 0),
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
                (0, 255, 255),
                ]
LINES_HASH_DIVIDER = 50


class Board:
    def __init__(self):
        self.lines = {}
        self.batch = pyglet.graphics.Batch()
        pyglet.gl.glClearColor(*BACKGROUND_COLOR)
        self.create_grid(GRID_WIDTH)
        self.paint_colors = PAINT_COLORS
        self.active_color = self.paint_colors[0]
        self.color_chooser = None
        self.current_page = 0
        self.pages = []

    def clean_page(self):
        self.lines = {}
        self.batch = pyglet.graphics.Batch()
        self.create_grid(GRID_WIDTH)

    def down(self):
        self.jump_page(self.current_page + 1)

    def up(self):
        if self.current_page > 0:
            self.jump_page(self.current_page - 1)

    def jump_page(self, new_page):
        try:
            self.pages[self.current_page] = {'lines': self.lines, 'batch': self.batch}
        except IndexError:
            self.pages.append({'lines': self.lines, 'batch': self.batch})

        try:
            self.lines = self.pages[new_page]['lines']
            self.batch = self.pages[new_page]['batch']
            self.create_grid(GRID_WIDTH)
        except IndexError:
            self.clean_page()

        self.current_page = new_page

    def create_grid(self, size):
        self.grid = []
        i = get_max_screens_height()
        while i > 0:
            line = pyglet.shapes.Line(0, i, get_max_screens_width(), i, width=1, color=GRID_COLOR, batch=self.batch)
            self.grid.append(line)
            i -= size
        i = 0
        while i < get_max_screens_width():
            i += size
            line = pyglet.shapes.Line(i, 0, i, get_max_screens_height(), width=1, color=GRID_COLOR, batch=self.batch)
            self.grid.append(line)

    def draw(self):
        self.batch.draw()

    def add(self, p1, p2, width):
        if p1 == p2:
            line = pyglet.shapes.Circle(p1[0], p1[1], radius=width / 2, color=self.active_color, batch=self.batch)
        else:
            line = pyglet.shapes.Line(p1[0], p1[1], p2[0], p2[1], width=width, color=self.active_color,
                                      batch=self.batch)
        self.store(line)

    def store(self, line):
        """allows us to delete lines in O(1)"""
        key = (line.x // LINES_HASH_DIVIDER, line.y // LINES_HASH_DIVIDER)
        l = self.lines.get(key, [])
        l.append(line)
        self.lines[key] = l

    def short_distance(self, obj1, obj2, threshold):
        try:
            return math.dist(obj1, [obj2.x, obj2.y]) < threshold or \
                   math.dist(obj1, [obj2.x2, obj2.y2]) < threshold
        except AttributeError:
            return math.dist(obj1, [obj2.x, obj2.y]) < threshold

    def remove(self, x, y, threshold):
        key_x, key_y = x // LINES_HASH_DIVIDER, y // LINES_HASH_DIVIDER
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                key = (key_x + i, key_y + j)
                l = self.lines.get(key, [])
                for line in l:
                    if self.short_distance((x, y), line, threshold):
                        l.remove(line)
                self.lines[key] = l

    def update_pen_color(self, color):
        self.active_color = color
