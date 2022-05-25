# TODO: better colors to choose from
# TODO: replace 'clean page' with 'delete page'
# TODO: PyInstaller + NSIS
# TODO: undo + redo
# TODO: readme

# TODO: change brush size
# TODO: don't change mouse cursor on menu
# TODO: does save/load restore an exact copy?
# TODO: clickable buttons picture
# TODO: return focus to main window after save/restore/pdf
# TODO: improve PDF quality?
# TODO: circlized lines - with varying pressure


import pyglet
from pyglet.window import key

import tablet
from board import Board
from mouse_cursor import change_mouse_cursor
from color_chooser import ColorChooser
from misc import disable_exit_on_esc_key
from help import show_help

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

window = pyglet.window.Window(1200, 900, caption="PenBoard", resizable=True)

board = Board(window)
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
    if (modifiers & key.MOD_ALT) or (modifiers & key.MOD_WINDOWS):
        return

    if symbol == key.DOWN:
        board.down()
    elif symbol == key.UP:
        board.up()
    elif symbol == key.C and not (modifiers & key.MOD_CTRL):
        ColorChooser(board, window.width / 2, window.height / 2)
    elif symbol == key.D and modifiers & key.MOD_CTRL :
        board.erase_page()
    elif symbol == key.S and modifiers & key.MOD_CTRL:
        board.save()
    elif symbol == key.L and modifiers & key.MOD_CTRL:
        board.load()
    elif symbol == key.I and modifiers & key.MOD_CTRL:
        board.export_to_png(window)
    elif symbol == key.P and modifiers & key.MOD_CTRL:
        board.export_to_pdf(window)
    elif symbol == key.F1:
        show_help()
    elif symbol == key.Q and modifiers & key.MOD_CTRL:
        pyglet.app.exit()


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
    # without this if the mouse click is going all the way to ColorChooser.handle_click ,
    # making it impossible to open it with left clicking on toolbar
    if y < board.upper_y:
        if combined_buttons(button) == 'click':
            if board.color_chooser is not None:
                board.color_chooser.handle_click(x, y)
            else:
                change_mouse_cursor('pen', window, board)
                board.paint(pen.get('pressure', 0.4), x, y, (x, y))
                on_mouse_drag.prev_point = (x, y)
        elif combined_buttons(button) == 'erase':
            width = board.erase(pen.get('pressure', 0.5), x, y)
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
            board.paint(pen.get('pressure', 0.6), x, y, on_mouse_drag.prev_point)
        on_mouse_drag.prev_point = (x, y)
    elif combined_buttons(buttons) == 'erase':
        width = board.erase(pen.get('pressure', 0.5), x, y)
        change_mouse_cursor('eraser', window, board, width=width)


on_mouse_drag.prev_point = None


@window.event
def on_resize(width, height):
    board.clean_page()


@window.event
def on_draw():
    window.clear()
    board.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()
