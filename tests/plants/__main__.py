#/usr/bin/env python2

import math
import pygame
from pygame.locals import *

def draw_branch(surface, color, start, end, size):
    points = []
    points.append((start[0] - size / 1.5, start[1]))
    points.append((end[0] - size / 2, end[1]))
    points.append((end[0] + size / 2, end[1]))
    points.append((start[0] + size / 1.5, start[1]))
    pygame.draw.polygon(surface, color, points)

class Plant:
    def __init__(self, max_size):
        self.max_size = max_size

    def generate(self, surface, coords, seed, time_seed, depth = 0):
        x_coord = coords[0] + math.sin(seed * time_seed) * time_seed * 150
        y_coord = coords[1] + (math.cos(seed)*42 * time_seed * 8) - 50
        draw_branch(surface, 0x000000, coords, (x_coord, y_coord), int(time_seed * 42))
        # pygame.draw.line(surface, 0x000000, coords, (x_coord, y_coord), int(time_seed * 42))
        if time_seed <= 0:
            pygame.draw.circle(surface, 0x000000, (int(x_coord), int(y_coord)), depth * 10, depth)
            # print(depth)
        if time_seed > 0:
            self.generate(surface, (x_coord, y_coord), seed, time_seed - 0.1, depth + 1)
            self.generate(surface, (x_coord, y_coord), seed, time_seed - 0.2, depth + 1)

class LightningBoltGen:
    def __init__(self, max_size):
        self.max_size = max_size
        
    def generate(self, surface, coords, seed, time_seed):
        x_coord = coords[0] + math.sin(seed) * 50
        y_coord = coords[1] + abs(math.cos(seed) * 5) + 25
        pygame.draw.line(surface, 0x8080FF, coords, (x_coord, y_coord), int(time_seed * 10))
        pygame.draw.line(surface, 0x0000FF, coords, (x_coord, y_coord), int(time_seed * 5))
        if time_seed > 0:
            times = int(abs(math.sin(seed) * 3))
            times = 1 if times == 0 else times
            while times > 0:
                self.generate(surface, (x_coord, y_coord), math.sin(seed * times) * 10, time_seed - 0.05)
                times = times - 1
        

def print_degrade(surface, steps, _from, to):
    step = [(-_from[0] + to[0]) / steps, (-_from[1] + to[1]) / steps, (-_from[2] + to[2]) / steps]
    size = (1280, 720 / steps)
    pos = (0, 0)
    b = steps
    while steps:
        color = pygame.Color(_from[0] + step[0], _from[1] + step[1], _from[2] + step[2], 0)
        pygame.draw.rect(surface, color, pygame.Rect(pos, size))
        _from[0] = _from[0] + step[0]
        _from[1] = _from[1] + step[1]
        _from[2] = _from[2] + step[2]
        pos = (0, pos[1] + (720 / b))
        steps -= 1
import random
if __name__ == "__main__":
    pygame.init()

    win_size = (width, height) = 1280, 720
    screen = pygame.display.set_mode(win_size)

    ended = False

    plant = Plant(1.5)
    bolt = LightningBoltGen(42)
    i = 0.2
    j = 0
    seed = 42
    pos = (0, 50)
    trigger = False
    while not ended:
        # screen.fill(0x000000)
        if trigger:
            print_degrade(screen, 15, [0x15, 0x15, 0x15], [0x74, 0xB6, 0xA1])
        else:
            print_degrade(screen, 15, [0x74, 0xB6, 0xA1], [0xF6, 0x0A, 0x4F])
        pygame.draw.circle(screen, 0xFFED83, (640, 700), 121)
        pygame.draw.circle(screen, 0xFFE652, (640, 700), 95)
        pygame.draw.circle(screen, 0xFFDC08, (640, 700), 75)
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            if event.type == KEYDOWN:
                trigger = True
                seed = random.randint(50, 75)
                pos = (random.randint(280, 1000), pos[1])
                j = 0
        plant.generate(screen, (640, 700), 42, i)
        if trigger:
            j = j + 0.01
            bolt.generate(screen, pos, seed, j)
            if j > 0.8:
                trigger = False
        pygame.draw.circle(screen, 0x000000, (640, 900), 250)
        if i < 0.5:
            i = i + 0.001
        # print(i)
        pygame.display.flip()
        pygame.time.wait(10)
        
    
