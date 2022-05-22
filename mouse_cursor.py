import pyglet


class EraserMouseCursor(pyglet.window.MouseCursor):
    def __init__(self, width):
        self.width = width

    def draw(self, x, y):
        batch = pyglet.graphics.Batch()
        circle = pyglet.shapes.Circle(x, y, self.width, color=(200, 0, 0), batch=batch)
        circle.opacity = 128
        batch.draw()


def change_mouse_cursor(type, window, width=None):
    # if type in [window.CURSOR_CROSSHAIR,]:
    #     image = pyglet.image.load('pencil.png')
    #     cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
    if type == window.CURSOR_NO:
        cursor = EraserMouseCursor(width)
    else:
        cursor = window.get_system_mouse_cursor(type)
    window.set_mouse_cursor(cursor)
