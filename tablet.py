import pyglet


def open_tablet(window):
    tablets = pyglet.input.get_tablets()

    if tablets:
        num = 0
        name = tablets[num].name

        try:
            canvas = tablets[num].open(window)
        except pyglet.input.DeviceException:
            print('Failed to open tablet %d on window' % num)

        print('Opened %s.' % name)
        return canvas

    else:
        print('No tablets found.')
