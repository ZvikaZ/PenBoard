# TODO: icons bar (next, prev, color, save, load, pdf, clean, undo, quit, help)
# TODO: better colors to choose from
# TODO: keyboard shortcuts (explain how to choose color)
# TODO: change brush size
# TODO: does save/load restore an exact copy?
# TODO: undo
# TODO: readme

import pyglet
from pyglet.window import key

import tablet
from board import Board
from mouse_cursor import change_mouse_cursor
from color_chooser import ColorChooser
from misc import disable_exit_on_esc_key
import operations

window = pyglet.window.Window(1200, 900, caption="PenBoard", resizable=True)

board = Board()
canvas = tablet.open_tablet(window)
pen = {}

change_mouse_cursor('default', window, board)
disable_exit_on_esc_key(window)

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
                change_mouse_cursor('eraser', window, board, width=8)
            else:
                change_mouse_cursor('default', window, board)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.DOWN:
        board.down()
    elif symbol == key.UP:
        board.up()
    elif symbol == key.C:
        board.erase_page()
    elif symbol == key.S:
        board.save()
    elif symbol == key.L:
        board.load()
    elif symbol == key.P:
        board.export_to_pdf(window)
    else:
        ColorChooser(board, window.width / 2, window.height / 2)


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
        if board.color_chooser is not None:
            board.color_chooser.handle_click(x, y)
        else:
            change_mouse_cursor('pen', window, board)
            operations.paint(board, pen.get('pressure', 0.4), x, y, (x, y))
            on_mouse_drag.prev_point = (x, y)
    elif combined_buttons(button) == 'erase':
        width = operations.erase(board, pen.get('pressure', 0.5), x, y)
        change_mouse_cursor('eraser', window, board, width=width)
    elif combined_buttons(button) == 'select':
        ColorChooser(board, x, y)


@window.event
def on_mouse_release(x, y, button, modifiers):
    change_mouse_cursor('default', window, board)
    on_mouse_drag.prev_point = None


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if combined_buttons(buttons) == 'click':
        change_mouse_cursor('pen', window, board)
        if on_mouse_drag.prev_point is not None:
            operations.paint(board, pen.get('pressure', 0.6), x, y, on_mouse_drag.prev_point)
        on_mouse_drag.prev_point = (x, y)
    elif combined_buttons(buttons) == 'erase':
        width = operations.erase(board, pen.get('pressure', 0.5), x, y)
        change_mouse_cursor('eraser', window, board, width=width)


on_mouse_drag.prev_point = None


@window.event
def on_draw():
    window.clear()
    board.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()
