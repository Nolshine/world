#let there be plants!
from random import random, randrange

from vec2d import vec2d



class Seed:
    def __init__(self, pos, kind, genes = {}):
        self.pos = vec2d(pos[0]*1.0, pos[1]*1.0)
        if self.pos.x < 0:
            self.pos.x += 700
        elif self.pos.x > 700:
            self.pos.x -= 700
        self.dir = vec2d(0,1)
        self.kind = kind #this will be Grass for the first seeds
        self.sprout = False
        self.genes = genes

    def update(self,time):
        if not self.sprout:
            self.pos = self.pos + (self.dir*time*0.1)
        if self.pos.y > 400:
            self.pos.y = 400
            self.sprout = True




class Grass:
    def __init__(self, pos, genes):
        #expecting a vec2d by this point. All plants start as seeds,
        #and all seeds have a vec2d for their position.
        self.base = pos
        self.energy = 30
        self.dead = False
        self.breed = False
        self.age = 0
        self.breed_req = 60
        self.timer = 0
        #genetics go here
        if genes == {}:
            self.genes = {
                "height":random()*20.0,
                "pods":randrange(1,3),
                "max_age":120000 #lives for a minute
                }
        else:
            mutate = random()
            if mutate >= 0.7:
                up_down = random()
                if up_down >= 0.5:
                    amt = randrange(1,3)
                else:
                    amt = randrange(1,3)*(-1)
                genes["height"] += amt
                genes["pods"] += amt
                genes["max_age"] += amt*30
            self.genes = genes
        self.pods = []
        for i in range(self.genes["pods"]):
            self.pods.append(random()*self.genes["height"])

    def update(self, time):
        self.age += time
        self.timer += time
        if self.age >= self.genes["max_age"]:
            self.dead = True
        if self.energy <= 0:
            self.dead = True
        if timer >= 30000:
            self.breed = True
