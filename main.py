# TODO: colors
# TODO: scrolling/pages
# TODO: resizing

# TODO: undo
# TODO: save
# TODO: create PDF
# TODO: allow mouse with tablet
# TODO: change brush size
# TODO: readme

import pyglet

import tablet
from board import Board
from mouse_cursor import change_mouse_cursor
from operations import paint, erase

window = pyglet.window.Window(1200, 900, caption="PenBoard", fullscreen=False, resizable=False)

board = Board(window)
canvas = tablet.open_tablet(window)

if canvas is not None:
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
                change_mouse_cursor(window.CURSOR_NO, window, 8)


    on_motion.prev_point = None

else:
    # currently we take mouse events only if tablet isn't working
    # otherwise, when table is working, we get double events

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            change_mouse_cursor(window.CURSOR_CROSSHAIR, window)
            paint(board, 0.4, x, y, (x, y))
            on_mouse_drag.prev_point = (x, y)
        elif button == pyglet.window.mouse.RIGHT:
            width = erase(board, 0.5, x, y)
            change_mouse_cursor(window.CURSOR_NO, window, width)


    @window.event
    def on_mouse_release(x, y, button, modifiers):
        change_mouse_cursor(window.CURSOR_DEFAULT, window)
        on_mouse_drag.prev_point = None


    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if buttons == pyglet.window.mouse.LEFT:
            change_mouse_cursor(window.CURSOR_CROSSHAIR, window)
            if on_mouse_drag.prev_point is not None:
                paint(board, 0.6, x, y, on_mouse_drag.prev_point)
            on_mouse_drag.prev_point = (x, y)
        if buttons == pyglet.window.mouse.RIGHT:
            width = erase(board, 0.5, x, y)
            change_mouse_cursor(window.CURSOR_NO, window, width)


    on_mouse_drag.prev_point = None


@window.event
def on_draw():
    window.clear()
    board.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()
