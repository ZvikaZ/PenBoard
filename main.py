# TODO: eraser O(1)
# TODO: colors
# TODO: scrolling/pages
# TODO: resizing

# TODO: undo
# TODO: save
# TODO: create PDF

# TODO: mouse - color chooser
# TODO: change brush size
# TODO: readme

import pyglet

import tablet
from board import Board
from mouse_cursor import change_mouse_cursor
from color_chooser import ColorChooser
import operations

window = pyglet.window.Window(1200, 900, caption="PenBoard", fullscreen=False, resizable=False)

board = Board(window)
canvas = tablet.open_tablet(window)
pen = {}

if canvas is not None:
    @canvas.event
    def on_motion(cursor, x, y, pressure, tilt_x, tilt_y, buttons):
        global pen
        pen = {
            'cursor_name': cursor.name,
            'x': x,
            'y': y,
            'pressure': pressure,
            'buttons': buttons
        }
        if pressure == 0:
            if cursor.name == "Eraser":
                change_mouse_cursor(window.CURSOR_NO, window, 8)
            else:
                change_mouse_cursor(window.CURSOR_DEFAULT, window)


def combined_buttons(button):
    if pen == {} or pen['buttons'] == 0:
        if button == pyglet.window.mouse.LEFT:
            return 'click'
        elif button == pyglet.window.mouse.RIGHT:
            return 'erase'
        else:
            return ''
    else:
        if pen['buttons'] == 1:
            return 'click'
        elif (pen['buttons'] & 2) == 2 or pen['cursor_name'] == 'Eraser':
            return 'erase'
        elif (pen['buttons'] & 4) == 4:
            return 'select'
        else:
            return ''


@window.event
def on_mouse_press(x, y, button, modifiers):
    if combined_buttons(button) == 'click':
        change_mouse_cursor(window.CURSOR_CROSSHAIR, window)
        operations.paint(board, pen.get('pressure', 0.4), x, y, (x, y))
        on_mouse_drag.prev_point = (x, y)
    elif combined_buttons(button) == 'erase':
        width = operations.erase(board, pen.get('pressure', 0.5), x, y)
        change_mouse_cursor(window.CURSOR_NO, window, width)
    elif combined_buttons(button) == 'select':
        ColorChooser(board, x, y)


@window.event
def on_mouse_release(x, y, button, modifiers):
    change_mouse_cursor(window.CURSOR_DEFAULT, window)
    on_mouse_drag.prev_point = None


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if combined_buttons(buttons) == 'click':
        change_mouse_cursor(window.CURSOR_CROSSHAIR, window)
        if on_mouse_drag.prev_point is not None:
            operations.paint(board, pen.get('pressure', 0.6), x, y, on_mouse_drag.prev_point)
        on_mouse_drag.prev_point = (x, y)
    elif combined_buttons(buttons) == 'erase':
        width = operations.erase(board, pen.get('pressure', 0.5), x, y)
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
