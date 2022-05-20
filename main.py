import pyglet
import sys

window = pyglet.window.Window(1024, 768, caption="PenBoard", resizable=True)
batch = pyglet.graphics.Batch()
pyglet.gl.glClearColor(0.9, 0.9, 0.9, 1.0)

tablets = pyglet.input.get_tablets()
canvases = []

points = []

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


@canvas.event
def on_motion(cursor, x, y, pressure, tilt_x, tilt_y):
    if pressure:
        print('%s: on_motion(%r, %r, %r, %r, %r, %r)' % (name, cursor, x, y, pressure, tilt_x, tilt_y))
        point = pyglet.shapes.Circle(x=x, y=y, radius=6, color=(0, 0, 0), batch=batch)
        points.append(point)


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()
