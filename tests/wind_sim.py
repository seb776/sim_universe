#!/usr/bin/env python2

import pygame
from pygame.color import *
from pygame.locals import *


def calc_new_vec(ivec, values):
    vec = [ivec[0], ivec[1]]
    magic = 0.98
    for v in values:
        if v is not None:
            vec[0] += v[0] * magic
            vec[1] += v[1] * magic
    return (float(vec[0]) / len(values), float(vec[1]) / len(values))

def calc_new_wind_map(_map):
    nmap = [[(0, 0) for x in range(5)] for x in range(20)]
    for i, line in enumerate(_map):
        for j, case in enumerate(line):
            nmap[i][j] = calc_new_vec(_map[i][j],
                                      [None if i - 1 < 0 else _map[i - 1][j],
                                       None if i - 1 < 0 or j - 1 < 0 else _map[i - 1][j - 1],
                                       None if j - 1 < 0 else _map[i][j - 1],
                                       None if i + 1 >= len(_map) or j - 1 < 0 else _map[i + 1][j - 1],
                                       None if i + 1 >= len(_map) else _map[i + 1][j],
                                       None if i + 1 >= len(_map) or j + 1 >= len(_map[i]) else _map[i + 1][j + 1],
                                       None if j + 1 >= len(_map[i]) else _map[i][j + 1],
                                       None if i - 1 < 0 or j + 1 >= len(_map[i]) else _map[i - 1][j + 1]
                                   ])
    return nmap

def draw_wind_map(_map):
    for line in _map:
        print(line)
    print()
            

def draw_wind_vec(srfc, _map):
    for i, line in enumerate(_map):
        for j, case in enumerate(line):
            pygame.draw.lines(srfc, THECOLORS["green"], False, [(i * 50 + 150, j * 50 + 150), (150 + i * 50 + case[0] * 20, 150 + j * 50 + case[1] * 20)], 2)
            pygame.draw.circle(srfc, THECOLORS["blue"], (i * 50 + 150, j * 50 + 150), 5, 0)
import random
if __name__ == "__main__":
    windList = [[(0, 0) for x in range(5)] for x in range(20)]

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    # windList[0][0] = (5, 6)
    # windList[0][1] = (150.0, 300.0)
    i = 0
    trigger = True
    val = (0, 0)
    val2 = (0, 0)
    while True:
        i += 1
        if i % 5 == 0:
            val = (random.randint(20, 40), random.randint(-40, 40))
            val2 = (random.randint(-40, -20), random.randint(-40, 40))
        windList[0][0] = val
        windList[18][3] = val2
        # draw_wind_map(windList)
        screen.fill(THECOLORS["white"])
        draw_wind_vec(screen, windList)
        windList = calc_new_wind_map(windList)
        pygame.time.wait(200)
        pygame.display.flip()
        # print("\033[0;0H")
