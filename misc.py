import pyglet


def get_max_screens_width():
    return max([s.width for s in pyglet.canvas.get_display().get_screens()])


def get_max_screens_height():
    return max([s.height for s in pyglet.canvas.get_display().get_screens()])
