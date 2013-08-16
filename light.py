#let there be light
from math import sin
from random import random, randrange

from vec2d import vec2d




class Light:
    def __init__(self, seed):
        self.pos = vec2d(random()*700, (-5.0))
        self.dir = vec2d(0.0, 1.0)
        self.dir = self.dir.rotated(sin(seed))
        self.energy = randrange(10,101)
        self.dead = False

    def update(self, time):
        self.pos = self.pos + ((self.dir)*time*0.5)
        if self.pos.y > 400:
            self.dead = True
        if self.pos.x < 0 or self.pos.x > 700:
            self.dir.x *= (-1)
