# TODO: colors
# TODO: scrolling/pages
# TODO: resizing

# TODO: undo
# TODO: mouse
# TODO: save
# TODO: create PDF
# TODO: readme

import pyglet

import tablet
from board import Board
from mouse_cursor import change_mouse_cursor
from operations import paint, erase

window = pyglet.window.Window(1200, 900, caption="PenBoard", fullscreen=False, resizable=False)

board = Board(window)
canvas = tablet.open_tablet(window)


@canvas.event
def on_motion(cursor, x, y, pressure, tilt_x, tilt_y):
    if pressure and cursor.name == 'Pressure Stylus':
        change_mouse_cursor(window.CURSOR_CROSSHAIR, window)
        if on_motion.prev_point is not None:
            paint(board, pressure, x, y, on_motion.prev_point)
        on_motion.prev_point = (x, y)
    else:
        change_mouse_cursor(window.CURSOR_DEFAULT, window)
        on_motion.prev_point = None
    if cursor.name == "Eraser":
        if pressure:
            width = erase(board, pressure, x, y)
            change_mouse_cursor(window.CURSOR_NO, window, width)
        else:
            change_mouse_cursor(window.CURSOR_NO, window, 10)


on_motion.prev_point = None


@window.event
def on_mouse_press(x, y, button, modifiers):
    print('press', x, y, button, modifiers)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print('drag', x, y, buttons, modifiers)


@window.event
def on_draw():
    window.clear()
    board.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()
