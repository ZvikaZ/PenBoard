import pyglet


class EraserMouseCursor(pyglet.window.MouseCursor):
    def __init__(self, width):
        self.width = width

    def draw(self, x, y):
        batch = pyglet.graphics.Batch()
        circle = pyglet.shapes.Circle(x, y, self.width, color=(200, 0, 0), batch=batch)
        circle.opacity = 128
        batch.draw()
