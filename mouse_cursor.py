import pyglet


class EraserMouseCursor(pyglet.window.MouseCursor):
    def __init__(self, width):
        self.width = width

    def draw(self, x, y):
        batch = pyglet.graphics.Batch()
        circle = pyglet.shapes.Circle(x, y, self.width, color=(200, 0, 0), batch=batch)
        circle.opacity = 128
        batch.draw()

class ColoredMouseCursor(pyglet.window.MouseCursor):
    def __init__(self, color):
        self.color = color
        self.size = 40
        self.width = 3

    def draw(self, x, y):
        batch = pyglet.graphics.Batch()
        self.line1 = pyglet.shapes.Line(x-self.size/2, y, x+self.size/2, y, width=self.width, color=self.color, batch=batch)
        self.line2 = pyglet.shapes.Line(x, y-self.size/2, x, y+self.size/2,  width=self.width, color=self.color, batch=batch)
        batch.draw()


def change_mouse_cursor(type, window, board, width=None):
    if type == 'eraser':
        cursor = EraserMouseCursor(width)
    elif type == 'pen':
        cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
    elif type == 'wait':
        cursor = window.get_system_mouse_cursor(window.CURSOR_WAIT)
    elif type == 'default':
        cursor = ColoredMouseCursor(board.active_color)
    else:
        raise ValueError("Unsupported cursor: " + type)
    window.set_mouse_cursor(cursor)
