import pyglet
from PIL import Image


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


def shape_to_dict(shape):
    # I don't care about anchors, and maybe some other important (to some other use cases) fields
    kind = type(shape).__name__
    result = {'kind': kind,
              'x': shape.x,
              'y': shape.y,
              'color': shape.color,
              'opacity': shape.opacity}
    if kind == 'Circle':
        result['radius'] = shape.radius
    elif kind == 'Line':
        result['x2'] = shape.x2
        result['y2'] = shape.y2
        result['width'] = shape._width
    else:
        raise ValueError('Unhandled "shape_to_dict" type: ' + kind)
    return result


def dict_to_shape(shape, batch):
    if shape['kind'] == 'Circle':
        obj = pyglet.shapes.Circle(shape['x'], shape['y'], radius=shape['radius'], color=shape['color'], batch=batch)
    elif shape['kind'] == 'Line':
        obj = pyglet.shapes.Line(shape['x'], shape['y'], shape['x2'], shape['y2'], width=shape['width'], color=shape['color'], batch=batch)
    else:
        raise ValueError('Unhandled "dict_to_shape" type: ' + shape['kind'])
    obj.opacity = shape['opacity']
    return obj


def pngs_to_pdf(input_pngs, output_pdf):
    # the image is RGBA. pillow cannot save RGBA as pdf, only RGB. so let's remove the alpha
    # from https://stackoverflow.com/questions/66311997/why-do-i-get-cannot-save-mode-rgba-error-when-using-pil
    rgb_pngs = []
    for input_png in input_pngs:
        png = Image.open(input_png)
        png.load()

        rgb_png = Image.new("RGB", png.size, (255, 255, 255))
        rgb_png.paste(png, mask=png.split()[3])  # 3 is the alpha channel
        rgb_pngs.append(rgb_png)

    # from https://stackoverflow.com/a/47283224/1543290
    rgb_pngs[0].save(output_pdf, "PDF", resolution=100.0, save_all=True, append_images=rgb_pngs[1:])

