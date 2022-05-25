import pyglet

HEIGHT = 680
WIDTH = 640
MARGIN = 30
HELP_BACKGROUND_COLOR = (1.0, 1.0, 1.0, 1.0)
HELP_TEXT_COLOR = (0, 0, 0, 255)
HELP_FONT = 'Segoe UI'
HELP_STR = '''Welcome to PenBoard!
By Zvika Haramaty     https://github.com/ZvikaZ/PenBoard

PenBoard is recommended to use with a pen tablet (such as Wacom devices), but also supports mouse usage.

PEN INSTRUCTIONS:
- touch the pen to the tablet to paint (according to the pressure)
- click the first pen button to erase (according to the pressure) 
- click the second pen button to open color palette chooser
- touch any button to operate it (as if the pen is a mouse)

TOOLBAR: explained from left to right (with keyboard shortcuts)
- this help screen (F1)
- color palette chooser (C)
- previous page (UP ARROW)
- next page (DOWN ARROW)
- save (CTRL-S)
- load (CTRL-L)
- save page as image (CTRL-I)
- export to PDF (CTRL-P)
- erase current page's contents (CTRL-D)
- quit (CTRL-Q)

* Note that there are no confirmations for any action
* Beware - this is an early release; it might suddenly crush; your saves might not be loaded; etc.
* We'd love to hear from you at https://github.com/ZvikaZ/PenBoard/issues
* Toolbar Icons downloaded from https://icons8.com/ 

* Click the mouse, or press any key, to dismiss this window
'''

help_window = None


def show_help():
    global help_window
    help_window = pyglet.window.Window(WIDTH, HEIGHT, resizable=True)
    pyglet.gl.glClearColor(*HELP_BACKGROUND_COLOR)
    label = pyglet.text.Label(HELP_STR, font_name=HELP_FONT, multiline=True,
                              x=MARGIN, width=WIDTH - MARGIN * 2, y=HEIGHT - MARGIN,
                              color=HELP_TEXT_COLOR)


    @help_window.event
    def on_draw():
        help_window.clear()
        label.draw()

    @help_window.event
    def on_mouse_press(x, y, button, modifiers):
        help_window.close()

    @help_window.event
    def on_key_press(symbol, modifiers):
        help_window.close()

    @help_window.event
    def on_resize(width, height):
        help_window.clear()
        label.draw()
