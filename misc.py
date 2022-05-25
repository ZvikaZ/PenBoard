import pyglet
from PIL import Image


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
        obj = pyglet.shapes.Line(shape['x'], shape['y'], shape['x2'], shape['y2'], width=shape['width'],
                                 color=shape['color'], batch=batch)
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


def get_points_in_line(x1, y1, x2, y2):
    x_min = min(x1, x2)
    x_max = max(x1, x2)
    y_min = min(y1, y2)
    y_max = max(y1, y2)
    if x1 == x2:
        return [(x1, y) for y in range(y_min, y_max + 1)]
    elif y1 == y2:
        return [(x, y1) for x in range(x_min, x_max + 1)]
    elif abs(x2 - x1) > abs(y2 - y1):
        if x_min == x1:
            y_start = y1
            y_end = y2
        else:
            y_start = y2
            y_end = y1
        rate = (y_end - y_start) / (x_max - x_min)
        return [(x, y_start + i * rate) for i, x in enumerate(range(x_min, x_max + 1))]
    else:
        if y_min == y1:
            x_start = x1
            x_end = x2
        else:
            x_start = x2
            x_end = x1
        rate = (x_end - x_start) / (y_max - y_min)
        return [(x_start + i * rate, y) for i, y in enumerate(range(y_min, y_max + 1))]


if __name__ == '__main__':
    import random

    print(get_points_in_line(6, 1, 8, 0))

    for i in range(100):
        a = 0
        b = 10
        x1 = random.randint(a, b)
        y1 = random.randint(a, b)
        x2 = random.randint(a, b)
        y2 = random.randint(a, b)
        print(f'({x1},{y1})->({x2},{y2}): {get_points_in_line(x1, y1, x2, y2)}')
