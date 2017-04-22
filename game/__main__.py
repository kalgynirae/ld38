#!/usr/bin/env python3
from collections import defaultdict
import enum
from functools import partial
import itertools

import pyglet
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.window import key, Window

from . import maps

fps = 30

class Dir:
    sw, w, nw, s, none, n, se, e, ne = itertools.product(range(-1, 2), repeat=2)

class Color:
    black = (0, 0, 0, 255)
    white = (255, 255, 255, 255)

movement = {
    'h': Dir.w,
    'j': Dir.s,
    'k': Dir.n,
    'l': Dir.e,
    key.MOTION_LEFT: Dir.w,
    key.MOTION_DOWN: Dir.s,
    key.MOTION_UP: Dir.n,
    key.MOTION_RIGHT: Dir.e,
}
_push = [5, 5, 5, 5, 5, 4, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]
#_push = [5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1]
gridsize = sum(_push)
width, height = 1280, 720
center = {'x': width // 2, 'y': height // 2}
gridwidth = width // gridsize
gridheight = height // gridsize
gridxoffset = (width - gridwidth * gridsize) // 2 + gridsize // 2
gridyoffset = (height - gridheight * gridsize) // 2 + gridsize // 2
images = {}
images['bg'] = pyglet.image.load('art/bg.png')
images['fish-left'] = pyglet.image.load('art/fish-left.png').get_texture()
images['fish-right'] = images['fish-left'].get_transform(flip_x=True)
images['fish-front'] = pyglet.image.load('art/fish-front.png').get_texture()
images['field-yellow'] = pyglet.image.load('art/field-yellow.png').get_texture()
images['field-red'] = pyglet.image.load('art/field-red.png').get_texture()
images['field-purple'] = pyglet.image.load('art/field-purple.png').get_texture()
images['bubble1'] = pyglet.image.load('art/bubble1.png').get_texture()
images['bubble2'] = pyglet.image.load('art/bubble2.png').get_texture()
images['bubble3'] = pyglet.image.load('art/bubble3.png').get_texture()
images['bubble4'] = pyglet.image.load('art/bubble4.png').get_texture()
for image in images.values():
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

label = partial(
    Label,
    anchor_x='center',
    anchor_y='baseline',
    bold=True,
    font_size=8,
)


_to_update = []
_batches = defaultdict(pyglet.graphics.Batch)


class CollisionRect:
    def __init__(self, obj):
        self.x = obj.x - obj.width // 2
        self.y = obj.y - obj.height // 2
        self.width = obj.width - 32
        self.height = obj.height - 32


_collisions = set()
def collides(a, b):
    arect = CollisionRect(a)
    brect = CollisionRect(b)
    does_collide = all([
        arect.x < brect.width + brect.x,
        arect.x + arect.width > brect.x,
        arect.y < brect.height + brect.y,
        arect.y + arect.height > brect.y,
    ])
    if does_collide:
        if (a, b) in _collisions:
            return False
        else:
            _collisions.add((a, b))
            return True
    else:
        if (a, b) in _collisions:
            _collisions.remove((a, b))
        return False


class ObjBase:
    def place(self, x, y):
        pass

    def update(self, dt):
        pass


_collidables = []
class Collidable:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _collidables.append(self)

    def get_colliding_objs(self):
        for obj in _collidables:
            if collides(self, obj):
                yield obj

    def collision(self, other):
        pass

    def update(self, dt):
        for obj in self.get_colliding_objs():
            self.collision(obj)
            if isinstance(obj, Collidable):
                obj.collision(self)
        super().update(dt)


class Obj(Collidable, ObjBase):
    def __init__(self, *, name=None, width, height):
        super().__init__()
        _to_update.append(self)
        self._x, self._y = 0, 0
        self.width, self.height = width, height
        self.actions = {}
        self._ids = itertools.count()
        self.parts = []
        if name:
            self.parts.append(Label(text=name, offset=(0, height // 2 + 4)))
        else:
            self.labels = []

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def act(self, iterator, *, id=None):
        if id is None:
            id = next(self._ids)
        self.actions[id] = iterator

    def is_done(self):
        return True

    def place(self, x, y):
        for part in self.parts:
            if isinstance(part, ObjBase):
                part.place(x, y)
            else:
                part.x = x
                part.y = y
        self._x = x
        self._y = y
        super().place(x, y)

    def update(self, dt):
        for id, action in list(self.actions.items()):
            try:
                next(action)
            except StopIteration:
                del self.actions[id]
        super().update(dt)


class Label(ObjBase):
    def __init__(self, *, text, offset):
        super().__init__()
        self.labels = [
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.black),
            label(text, batch=_batches['label'], color=Color.white),
        ]
        self.shadowdirs = [
            Dir.w,
            Dir.s,
            Dir.n,
            Dir.e,
            Dir.nw,
            Dir.ne,
            Dir.se,
            Dir.sw,
            Dir.none,
        ]
        self.offset = offset

    def place(self, x, y):
        ox, oy = self.offset
        for label, (dx, dy) in zip(self.labels, self.shadowdirs):
            label.x = x + dx + ox
            label.y = y + dy + oy
        super().place(x, y)


class Fish(Obj):
    def __init__(self, *, batch=None, **kwargs):
        batch = batch or _batches[type(self).__name__.lower()]
        self.sprites = {
            'left': Sprite(images['fish-left'], batch=batch),
            'front': Sprite(images['fish-front'], batch=batch),
            'right': Sprite(images['fish-right'], batch=batch),
        }
        super().__init__(**kwargs, height=images['fish-left'].height, width=images['fish-left'].width)
        for sprite in self.sprites.values():
            self.parts.append(sprite)
            sprite.anchor_x = sprite.width // 2
            sprite.anchor_y = sprite.height // 2
            sprite.visible = False
        self.sprites['left'].visible = True
        self.direction = 'left'

    def face(self, direction):
        dx, _ = direction
        if dx == 0:
            return
        elif dx < 0:
            newdir = 'left'
        elif dx > 0:
            newdir = 'right'
        if newdir != self.direction:
            self.act(self.face_iter(newdir), id='face')
            self.direction = newdir

    def face_iter(self, dir):
        self.sprites['left'].visible = False
        self.sprites['right'].visible = False
        self.sprites['front'].visible = True
        yield
        yield
        self.sprites['front'].visible = False
        self.sprites[dir].visible = True

    def move(self, dir):
        if self.map.try_move(self, dir):
            self.act(self.move_iter(dir))

    def move_iter(self, dir):
        for amount in _push:
            dx, dy = dir
            new_x = self.x + dx*amount
            new_y = self.y + dy*amount
            self.place(new_x, new_y)
            yield


class Field(Obj):
    def __init__(self, *, batch=None, **kwargs):
        super().__init__(**kwargs, height=images['field-red'].height, width=images['field-red'].width)
        batch = batch or _batches[type(self).__name__.lower()]
        self.sprites = [
            Sprite(images['field-yellow'], batch=batch),
            Sprite(images['field-red'], batch=batch),
            Sprite(images['field-purple'], batch=batch),
        ]
        self.parts.extend(self.sprites)
        self.state = 0
        self.advance()

    def advance(self, state=None):
        if state is None:
            state = (self.state + 1) % len(self.sprites)
        for sprite in self.sprites:
            sprite.visible = False
        self.sprites[state].visible = True
        self.state = state

    def collision(self, other):
        self.advance()

    def is_done(self):
        return self.state == 2


class Bubble(Obj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, width=images['bubble1'].width, height=images['bubble1'].height)
        self.sprites = [
            Sprite(images['bubble1'], batch=_batches['bubble']),
            Sprite(images['bubble2'], batch=_batches['bubble']),
            Sprite(images['bubble3'], batch=_batches['bubble']),
            Sprite(images['bubble4'], batch=_batches['bubble']),
            Sprite(images['bubble3'], batch=_batches['bubble']),
            Sprite(images['bubble2'], batch=_batches['bubble']),
        ]
        self.parts.extend(self.sprites)
        self.frame = 0
        self.act(self.animate_iter())

    def animate_iter(self):
        while True:
            self.frame = (self.frame + 1) % len(self.sprites)
            for sprite in self.sprites:
                sprite.visible = False
            self.sprites[self.frame].visible = True
            for _ in range(3):
                yield


player = Fish(name='T. Jefferson')
window = Window(width, height)
bg = Sprite(images['bg'], **center)


class Map:
    def __init__(self, width, height):
        self.grid = defaultdict(set)
        self.width = width
        self.height = height

    def locate(self, obj):
        for loc, objs in self.grid.items():
            if obj in objs:
                return loc
        raise ValueError('{obj!r} is not in the grid')

    def try_move(self, obj, dir):
        dx, dy = dir
        gx, gy = self.locate(obj)
        nx = gx + dx
        ny = gy + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.grid[gx, gy].remove(obj)
            self.grid[nx, ny].add(obj)
            return True
        else:
            return False

    def put(self, obj, gx, gy):
        self.grid[gx, gy].add(obj)
        obj.map = self
        x = gx * gridsize + gridxoffset
        y = gy * gridsize + gridyoffset
        obj.place(x, y)

    def spawn(self, type, gx, gy):
        self.put(type(), gx, gy)

map = Map(gridwidth, gridheight)
for (gx, gy), char in maps.parse(maps.map1):
    if char == '#':
        map.spawn(Field, gx, gy)
    elif char == 's':
        map.put(player, gx, gy)
    elif char == 'o':
        map.spawn(Bubble, gx, gy)

def check_done(dt):
    if all(obj.is_done() for objs in map.grid.values() for obj in objs):
        print('done!')
pyglet.clock.schedule_interval(check_done, 10 / fps)


def exit(dt):
    window.close()
    pyglet.app.exit()

@window.event
def on_draw():
    window.clear()
    bg.draw()
    _batches['field'].draw()
    _batches['fish'].draw()
    _batches['bubble'].draw()
    _batches['label'].draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol in [key.ESCAPE]:
        pyglet.clock.schedule(exit)

@window.event
def on_text(text):
    if text in ['q']:
        pyglet.clock.schedule(exit)
    elif text in movement:
        player.move(movement[text])
        player.face(movement[text])
    else:
        print(f'text {text!r}')

@window.event
def on_text_motion(motion):
    on_text(motion)

def update(dt):
    for obj in _to_update:
        obj.update(dt)

pyglet.clock.schedule_interval(update, 1 / fps)
pyglet.app.run()
