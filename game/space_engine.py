#!/usr/bin/env python2

import pygame
from pygame.locals import *
from pygame.color import *

class GameData:
    def __init__(self):
        self.background = None
        self.objects = []

    def load(self):
        self.background = pygame.image.load("ressources/space.png")
        self.gravity_center = []
        self.under_gravity = []

class SpaceEngine:
    def __init__(self, screen_size, title = "SpaceEngine"):
        pygame.display.init()
        pygame.font.init()

        self.screen = None
        self.size = screen_size
        self.title = title
        self.font = pygame.font.Font(pygame.font.get_default_font(), 15)

    def start(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.main_menu()

    def main_menu(self):
        img = pygame.image.load("ressources/gas_giant.png")
        in_game = True
        ended = False
        while in_game:
            self.screen.blit(img, (0, 0))
            pygame.display.flip()
            while not ended:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return
                        ended = True
            in_game = self.start_game()
            ended = False

    def load_screen(self, idx = 0):
        self.screen.fill(0x000000)
        text = self.font.render("Loading", True, THECOLORS["blue"])
        self.screen.blit(text, (self.size[0] / 2, self.size[1] / 2))
        pygame.display.flip()

    def start_game(self):
        self.load_screen()
        game_data = GameData()
        game_data.load()

        ended = False
        while not ended:
            self.screen.blit(game_data.background, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return True
            pygame.display.flip()
