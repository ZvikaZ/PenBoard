# TODO: eraser
# TODO: colors
# TODO: scrolling
# TODO: grid
# TODO: undo

import pyglet
import sys

window = pyglet.window.Window(1200, 900, caption="PenBoard", resizable=True)
batch = pyglet.graphics.Batch()
pyglet.gl.glClearColor(0.9, 0.9, 0.9, 1.0)

tablets = pyglet.input.get_tablets()
canvases = []

lines = []

if tablets:
    print('Tablets:')
    for i, tablet in enumerate(tablets):
        print('  (%d) %s' % (i + 1, tablet.name))

    num = 0
    name = tablets[num].name

    try:
        canvas = tablets[num].open(window)
    except pyglet.input.DeviceException:
        print('Failed to open tablet %d on window' % num)
        sys.exit(1)

    print('Opened %s' % name)


else:
    print('No tablets found.')
    sys.exit(1)


def change_mouse_cursor(type):
    # if type in [window.CURSOR_CROSSHAIR,]:
    #     image = pyglet.image.load('pencil.png')
    #     cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
    #     window.set_mouse_cursor(cursor)
    # else:
    window.set_mouse_cursor(window.get_system_mouse_cursor(type))


@canvas.event
def on_motion(cursor, x, y, pressure, tilt_x, tilt_y):
    if pressure and cursor.name == 'Pressure Stylus':
        change_mouse_cursor(window.CURSOR_CROSSHAIR)
        if on_motion.prev_point is not None:
            x2, y2 = on_motion.prev_point
            width = 6 * (pressure / 2 + 0.5)
            line = pyglet.shapes.Line(x, y, x2, y2, width=width, color=(0, 0, 0), batch=batch)
            lines.append(line)
        on_motion.prev_point = (x, y)
    else:
        change_mouse_cursor(window.CURSOR_DEFAULT)
        on_motion.prev_point = None
    if cursor.name == "Eraser":
        change_mouse_cursor(window.CURSOR_NO)


on_motion.prev_point = None


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()
