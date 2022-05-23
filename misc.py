import pyglet


def get_max_screens_width():
    return max([s.width for s in pyglet.canvas.get_display().get_screens()])


def get_max_screens_height():
    return max([s.height for s in pyglet.canvas.get_display().get_screens()])


def disable_exit_on_esc_key(window):
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            return True

    # I have no idea why, but if it's only once - it's ignored. strange...
    window.push_handlers(on_key_press)
    window.push_handlers(on_key_press)
