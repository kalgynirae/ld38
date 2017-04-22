#!/usr/bin/env python3
from functools import partial

import pyglet
from pyglet.graphics import Batch
from pyglet.text import Label
from pyglet.sprite import Sprite
from pyglet.window import key, Window

fps = 30
left, down, up, right = (-1, 0), (0, -1), (0, 1), (1, 0)
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
    if name != 'bg':
        i.anchor_x = i.width // 2
        i.anchor_y = i.height // 2
    images[name] = i

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

class Fish:
    def __init__(self, name):
        self.label = label(name, batch=sprite_batch)
        self.sprites = [
            Sprite(
                images['fish'],
                batch=sprite_batch,
            ),
            Sprite(
                images['fish'].get_transform(flip_x=True),
                batch=sprite_batch,
            ),
        ]

    def move(self, x, y):
        self.sprite.x = x
        self.sprite.y = y
        self.label.x = x
        self.label.y = y + self.sprite.height // 2 + 4

    @property
    def x(self):
        return self.sprite.x

    @property
    def y(self):
        return self.sprite.y


actions = []
player = Fish('T. Jefferson')
player.move(**centered)
window = Window(width, height)
bg = Sprite(images['bg'])


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
        actions.append(move(player, movement[symbol], push()))
    else:
        print(symbol)

def update(dt):
    still_go = []
    for action in actions:
        try:
            next(action)
        except StopIteration:
            pass
        else:
            still_go.append(action)
    actions[:] = still_go

pyglet.clock.schedule_interval(update, 1 / fps)
pyglet.app.run()
