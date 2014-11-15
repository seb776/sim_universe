#!/usr/bin/env python2

import pygame
from pygame.locals import *
from pygame.color import *

from game_instance import *

class Game:
    def __init__(self, screen_size, title = "SpaceEngine"):
        pygame.display.init()
        pygame.font.init()

        self.screen = None
        self.size = screen_size
        self.title = title
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)

    def start(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.main_menu()

    def show_menu(self, surface, current, items):
        coords = (50, 250)
        for idx, item in enumerate(items):
            surf = self.font.render(item, True, THECOLORS["blue"] if current != idx else THECOLORS["red"])
            surface.blit(surf, coords)
            coords = (coords[0], coords[1] + 50)

    def main_menu(self):
        img = pygame.image.load("ressources/gas_giant.png")
        in_game = True
        ended = False
        menu_idx = 0
        choice = [
            self.start_game,
            self.options,
            self.quit
        ]
        buttons = [
            "Start game!",
            "Options",
            "Quit"
        ]
        while in_game:
            while not ended:
                self.screen.blit(img, (0, 0))
                self.show_menu(self.screen, menu_idx, buttons)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return
                        if event.key == K_RETURN:
                            ended = True
                        if event.key == K_UP and menu_idx > 0:
                            menu_idx -= 1
                        if event.key == K_DOWN and menu_idx < len(choice) - 1:
                            menu_idx += 1
                        print(menu_idx)
            in_game = choice[menu_idx]()
            ended = False

    def load_screen(self, idx = 0):
        self.screen.fill(0x000000)
        text = self.font.render("Loading", True, THECOLORS["blue"])
        self.screen.blit(text, (self.size[0] / 2, self.size[1] / 2))
        pygame.display.flip()

    def options(self):
        return True

    def quit(self):
        return False

    def start_game(self):
        self.load_screen()
        game_instance = GameInstance()
        return game_instance.start()
