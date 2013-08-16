from random import random

import pygame
from pygame.locals import *

from vec2d import vec2d

from light import Light
from plants import *



def start():
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((700,450), DOUBLEBUF)

    paused = False
    frames = 0
    ground = pygame.Rect(0, 400, 700, 50)
    selection = Grass
    
    
    ground_day = (100,80,10)
    sky_day = (30,120,200)
    sun = [(255,255,128), (255,200,0)]
    white = (255,255,255)
    
    light = []
    seeds = []
    grass = []

    try:
        while True:
            time_passed = clock.tick(50)
            #event processing here.
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                    elif event.key == K_ESCAPE:
                        raise(KeyboardInterrupt)
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        seeds.append(Seed(pos, selection))

            frames += 1
            #I'll update entities here...
            if not paused:
                #light!
                chance = random()
                if chance > 0.4:
                    light.append(Light(frames))
                if light != []:
                    for photon in light:
                        photon.update(time_passed)
                        for plant in grass:
                            if photon.dead:
                                break
                            if plant.pods != []:
                                for y in plant.pods:
                                    rect = pygame.Rect((plant.base.x-2),
                                                       (plant.base.y-y-2),
                                                       4,
                                                       4)
                                    if rect.collidepoint(photon.pos):
                                        plant.energy += photon.energy
                                        photon.dead = True
                                        break

                        if photon.dead:
                            light.remove(photon)
                #seeds!
                if seeds != []:
                    for seed in seeds:
                        seed.update(time_passed)
                        if seed.sprout:
                            if seed.kind == Grass:
                                grass.append(seed.kind(seed.pos, seed.genes))
                            seeds.remove(seed)

                #grass!
                if grass != []:
                    for plant in grass:
                        plant.update(time_passed)
                        if plant.breed and len(grass) < 250:
                            pos_x = plant.base.x
                            for y in plant.pods:
                                plant.energy -= plant.breed_req
                                if plant.energy <= 0:
                                    plant.dead = True
                                    break
                                pos_y = plant.base.y-y
                                dx = randrange(5,11)*y
                                seeds.append(Seed((pos_x-dx, pos_y),
                                                  Grass,
                                                  plant.genes))
                                seeds.append(Seed((pos_x+dx, pos_y),
                                                  Grass,
                                                  plant.genes))
                        if plant.dead:
                            grass.remove(plant)
            
            #display stuff here.
            screen.fill(sky_day)
            screen.fill(ground_day ,ground)
            pygame.draw.circle(screen, sun[1], (65,65), 10)
            pygame.draw.circle(screen, sun[0], (65,65), 5)

##            if light != []:
##                for photon in light:
##                            pygame.draw.circle(screen,
##                                               white,
##                                               (int(round(photon.pos[0])),
##                                                int(round(photon.pos[1]))),
##                                               1)
            if seeds != []:
                for seed in seeds:
                    pygame.draw.circle(screen,
                                       (40,30,0),
                                       (int(round(seed.pos[0])),
                                        int(round(seed.pos[1]))),
                                       1)

            if grass != []:
                for plant in grass:
                    pygame.draw.line(screen,
                                     (13,75,0),
                                     plant.base,
                                     (plant.base[0],
                                      plant.base[1]-plant.genes["height"]),
                                     1)
                    for y in plant.pods:
                        pygame.draw.circle(screen,
                                           (80,100,0),
                                           (int(round(plant.base[0])),
                                            int(round(plant.base[1]-y))),
                                           2)
            
            pygame.display.set_caption(str(frames))
            pygame.display.update()
    except(KeyboardInterrupt):
        pygame.quit()


#It begins!
start()
