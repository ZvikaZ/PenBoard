import math
import pickle
import pyglet
import tempfile

from misc import *
import file_dialog
from mouse_cursor import change_mouse_cursor
from color_chooser import ColorChooser

BACKGROUND_COLOR = (1.0, 1.0, 1.0, 1.0)
GRID_COLOR = (200, 200, 200)
GRID_WIDTH = 60
PAINT_COLORS = [(0, 0, 0),
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
                (0, 255, 255),
                ]
CURRENT_PAGE_COLOR = (100, 0, 0, 255)
SHAPES_HASH_DIVIDER = 50


class Board:
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        pyglet.gl.glClearColor(*BACKGROUND_COLOR)
        self.paint_colors = PAINT_COLORS
        self.active_color = self.paint_colors[0]
        self.color_chooser = None
        self.current_page = 0
        self.pages = []
        self.pages.append({})
        self.create_grid(GRID_WIDTH)

    def get_current_shapes(self):
        return self.pages[self.current_page]

    def clean_page(self):
        self.batch = pyglet.graphics.Batch()
        self.create_grid(GRID_WIDTH)

    def down(self):
        self.jump_page(self.current_page + 1)

    def up(self):
        if self.current_page > 0:
            self.jump_page(self.current_page - 1)

    def jump_page(self, new_page):
        self.current_page = new_page
        while True:
            try:
                self.pages[self.current_page]
                break
            except IndexError:
                self.pages.append({})

        self.clean_page()

        shapes = self.update_batch(self.batch)
        self.pages[self.current_page] = shapes

    def create_grid(self, size):
        self.grid = []
        i = get_max_screens_height()
        while i > 0:
            line = pyglet.shapes.Line(0, i, get_max_screens_width(), i, width=1, color=GRID_COLOR, batch=self.batch)
            self.grid.append(line)
            i -= size
        i = 0
        while i < get_max_screens_width():
            i += size
            line = pyglet.shapes.Line(i, 0, i, get_max_screens_height(), width=1, color=GRID_COLOR, batch=self.batch)
            self.grid.append(line)
        self.create_toolbar()

    def create_toolbar(self):
        def help_button_handler():
            print("help")

        def color_button_handler():
            ColorChooser(self, self.window.width / 2, self.window.height / 2)

        def prev_button_handler():
            self.up()

        def next_button_handler():
            self.down()

        def save_button_handler():
            self.save()

        def load_button_handler():
            self.load()

        def pdf_button_handler():
            self.export_to_pdf(self.window)

        def clean_button_handler():
            self.erase_page()

        def close_button_handler():
            pyglet.app.exit()

        pngs_and_handlers = [
            ('icons8-help-48.png', help_button_handler),
            ('icons8-color-wheel-48.png', color_button_handler),
            ('icons8-back-to-48.png', prev_button_handler),
            ('icons8-next-page-48.png', next_button_handler),
            ('icons8-save-48.png', save_button_handler),
            ('icons8-opened-folder-48.png', load_button_handler),
            ('icons8-export-pdf-48.png', pdf_button_handler),
            ('icons8-paper-48.png', clean_button_handler),
            # 'icons8-undo-48.png',
            # 'icons8-redo-48.png',
            ('icons8-close-window-48.png', close_button_handler),
        ]

        x = 10
        y = self.window.height - 60
        self.frame = pyglet.gui.Frame(self.window, order=4)
        for png, handler in pngs_and_handlers:
            image = pyglet.resource.image(png)
            button = pyglet.gui.PushButton(x, y, pressed=image, depressed=image, batch=self.batch)
            button.set_handler('on_press', handler)
            self.frame.add_widget(button)
            x += 60

        self.grid.append(pyglet.text.Label(f'Page: {self.current_page + 1} of {len(self.pages)}',
                                           font_size=14,
                                           color=CURRENT_PAGE_COLOR,
                                           x=x,
                                           y=y + 10,
                                           batch=self.batch))

    def draw(self):
        self.batch.draw()

    def add(self, p1, p2, width):
        if p1 == p2:
            shape = pyglet.shapes.Circle(p1[0], p1[1], radius=width / 2, color=self.active_color, batch=self.batch)
        else:
            shape = pyglet.shapes.Line(p1[0], p1[1], p2[0], p2[1], width=width, color=self.active_color,
                                       batch=self.batch)
        self.store(shape)

    def store(self, shape):
        """allows us to delete a shape in O(1)"""
        key = (shape.x // SHAPES_HASH_DIVIDER, shape.y // SHAPES_HASH_DIVIDER)
        l = self.get_current_shapes().get(key, [])
        l.append(shape)
        self.get_current_shapes()[key] = l

    def short_distance(self, obj1, obj2, threshold):
        try:
            return math.dist(obj1, [obj2.x, obj2.y]) < threshold or \
                   math.dist(obj1, [obj2.x2, obj2.y2]) < threshold
        except AttributeError:
            return math.dist(obj1, [obj2.x, obj2.y]) < threshold

    def remove(self, x, y, threshold):
        key_x, key_y = x // SHAPES_HASH_DIVIDER, y // SHAPES_HASH_DIVIDER
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                key = (key_x + i, key_y + j)
                l = self.get_current_shapes().get(key, [])
                for shape in l:
                    if self.short_distance((x, y), shape, threshold):
                        l.remove(shape)
                self.get_current_shapes()[key] = l

    def update_pen_color(self, color):
        self.active_color = color

    def save(self):
        save_as = file_dialog.FileSaveDialog(initial_file="PenBoard",
                                             filetypes=[("PNB", ".pnb"), ("PenBoard", ".pnb")])
        filename = save_as._open_dialog(save_as._dialog)
        if filename:
            with open(filename, 'wb') as f:
                pickle.dump([list((k, [shape_to_dict(s) for s in p[k]])
                                  for k in p.keys()) for p in self.pages], f)

    def load(self):
        load_dialog = file_dialog.FileOpenDialog(filetypes=[("PNB", ".pnb"), ("PenBoard", ".bnb")])
        filename = load_dialog._open_dialog(load_dialog._dialog)
        with open(filename, 'rb') as f:
            self.pages = []
            for page in pickle.load(f):
                shapes = {}
                for key, section in page:
                    shapes[key] = [dict_to_shape(shape, self.batch) for shape in section]
                self.pages.append(shapes)
            self.jump_page(0)

    def export_to_pdf(self, window):
        save_as = file_dialog.FileSaveDialog(initial_file="PenBoard",
                                             filetypes=[("PDF", ".pdf"), ("", ".pdf")])
        filename = save_as._open_dialog(save_as._dialog)
        if filename:
            change_mouse_cursor('wait', window, self)
            current_page = self.current_page
            screenshot_pngs = []

            for page in range(len(self.pages)):
                self.current_page = page
                batch = pyglet.graphics.Batch()
                shapes = self.update_batch(batch)

                window.clear()
                batch.draw()

                screenshot_pngs.append(tempfile.NamedTemporaryFile(suffix='.png').name)
                pyglet.image.get_buffer_manager().get_color_buffer().save(screenshot_pngs[-1])

            pngs_to_pdf(screenshot_pngs, filename)

            self.current_page = current_page
            self.update_batch(self.batch)
            change_mouse_cursor('default', window, self)

    def update_batch(self, batch):
        # it's a little bit cumbersome - the idea is just to update the 'batch' property of every shape
        # I couldn't find direct means of doing it, so we go over all shapes, and re-create them with new batch
        shapes = {}
        for key in self.get_current_shapes():
            section = self.get_current_shapes()[key]
            shapes[key] = [dict_to_shape(shape_to_dict(shape), batch) for shape in section]
        return shapes

    def erase_page(self):
        self.pages[self.current_page] = {}
        self.clean_page()
