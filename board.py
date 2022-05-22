import math
import pyglet

BACKGROUND_COLOR = (1.0, 1.0, 1.0, 1.0)
GRID_COLOR = (200, 200, 200)
GRID_WIDTH = 60


class Board:
    def __init__(self, window):
        self.lines = []
        self.width = window.width
        self.height = window.height
        self.batch = pyglet.graphics.Batch()
        pyglet.gl.glClearColor(*BACKGROUND_COLOR)
        self.create_grid(GRID_WIDTH)

    def create_grid(self, size):
        self.grid = []
        i = self.height
        while i > 0:
            line = pyglet.shapes.Line(0, i, self.width, i, width=1, color=GRID_COLOR, batch=self.batch)
            self.grid.append(line)
            i -= size
        i = 0
        while i < self.width:
            i += size
            line = pyglet.shapes.Line(i, 0, i, self.height, width=1, color=GRID_COLOR, batch=self.batch)
            self.grid.append(line)

    def draw(self):
        self.batch.draw()

    def add(self, p1, p2, width):
        line = pyglet.shapes.Line(p1[0], p1[1], p2[0], p2[1], width=width, color=(0, 0, 0), batch=self.batch)
        self.lines.append(line)

    def remove(self, x, y, threshold):
        # this is O(n), can be easily changed to O(1) if it will show problems...
        for line in self.lines:
            if math.dist([x, y], [line.x, line.y]) < threshold or \
                    math.dist([x, y], [line.x2, line.y2]) < threshold:
                self.lines.remove(line)
