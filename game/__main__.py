#!/usr/bin/env python3
from functools import partial

import pyglet
from pyglet.graphics import Batch
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.window import key, Window

fps = 30
left, down, up, right, nodir = (-1, 0), (0, -1), (0, 1), (1, 0), (0, 0)
black, white = (0, 0, 0, 200), (255, 255, 255, 255)
movement = {
    key.H: left,
    key.J: down,
    key.K: up,
    key.L: right,
    key.LEFT: left,
    key.DOWN: down,
    key.UP: up,
    key.RIGHT: right,
}
width, height = 1280, 720
centered = {'x': width // 2, 'y': height // 2}
images = {}
images['bg'] = pyglet.image.load('art/bg.png')
images['fish-left'] = pyglet.image.load('art/fish-left.png').get_texture()
images['fish-right'] = images['fish-left'].get_transform(flip_x=True)
images['fish-front'] = pyglet.image.load('art/fish-front.png').get_texture()
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

sprite_batch = Batch()


def push():
    yield from iter([5, 5, 5, 5, 4, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1])

def move(obj, direction, multipliers):
    for multiplier in multipliers:
        dx, dy = direction
        new_x = obj.x + dx*multiplier
        new_y = obj.y + dy*multiplier
        obj.move(new_x, new_y)
        yield

to_update = []

class Fish:
    def __init__(self, name):
        self.labels = [
            label(name, batch=sprite_batch, color=black),
            label(name, batch=sprite_batch, color=black),
            label(name, batch=sprite_batch, color=black),
            label(name, batch=sprite_batch, color=black),
            label(name, batch=sprite_batch, color=white),
        ]
        self.sprites = {
            'left': Sprite(images['fish-left'], batch=sprite_batch),
            'front': Sprite(images['fish-front'], batch=sprite_batch),
            'right': Sprite(images['fish-right'], batch=sprite_batch),
        }
        for sprite in self.sprites.values():
            sprite.anchor_x = sprite.width // 2
            sprite.anchor_y = sprite.height // 2
            sprite.visible = False
        self.sprites['left'].visible = True
        self.direction = 'left'
        self.actions = []
        to_update.append(self)

    @property
    def x(self):
        return self.sprites['left'].x

    @property
    def y(self):
        return self.sprites['left'].y

    def move(self, x, y):
        for sprite in self.sprites.values():
            sprite.x = x
            sprite.y = y
        for label, offset in zip(self.labels, [left, down, up, right, nodir]):
            ox, oy = offset
            label.x = x + ox
            label.y = y + self.sprites['left'].height // 2 + 4 + oy

    def update(self, dt):
        oldx, oldy = self.x, self.y
        still_actions = []
        for action in self.actions:
            try:
                next(action)
            except StopIteration:
                pass
            else:
                still_actions.append(action)
        self.actions[:] = still_actions

        dx, dy = oldx - self.x, oldy - self.y
        if dx > 0:
            newdir = 'left'
        elif dx < 0:
            newdir = 'right'
        else:
            newdir = self.direction
        if newdir != self.direction:
            self.sprites[self.direction].visible = False
            self.sprites['front'].visible = True
        else:
            self.sprites[self.direction].visible = True
            self.sprites['front'].visible = False
        self.direction = newdir


actions = []
player = Fish('T. Jefferson')
player.move(**centered)
window = Window(width, height)
bg = Sprite(images['bg'], **centered)


@window.event
def on_draw():
    window.clear()
    bg.draw()
    sprite_batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol in [key.Q, key.ESCAPE]:
        pyglet.app.exit()
    elif symbol in movement:
        player.actions.append(move(player, movement[symbol], push()))
    else:
        print(symbol)

def update(dt):
    for obj in to_update:
        obj.update(dt)

pyglet.clock.schedule_interval(update, 1 / fps)
pyglet.app.run()
