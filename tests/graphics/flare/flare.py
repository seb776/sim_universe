#!/usr/bin/env python2

import math
import sys
import pygame
from pygame.color import *
from pygame.locals import *

def     main():
    pygame.init()

    width = 1280
    height = 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Universe")

    background = pygame.image.load("background.png")
    flare = pygame.image.load("flare.png")

    ended = False
    while not ended:
        for event in pygame.event.get():
            if event.type == KEYUP:
                pass
            if event.type == KEYDOWN:
                pass
                print(event.key)
        screen.blit(background, (-250, -250))
        pos = pygame.mouse.get_pos()
        npos = (pos[0] - 250, pos[1] - 125)
        screen.blit(flare, npos, None, BLEND_ADD)
        pygame.display.flip()
    

if __name__ == '__main__':
    sys.exit(main())
