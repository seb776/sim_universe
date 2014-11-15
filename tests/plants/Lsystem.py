#/usr/bin/env python2

import math
import pygame
from pygame.locals import *

class Plant:
    def turn_left(self, surface, length):
        self.current[2] -= 3.14 / (180 / 25)

    def turn_right(self, surface, length):
        self.current[2] += 3.14 / (180 / 25)

    def save_context(self, surface, length):
        self.contexts.insert(0, self.current)

    def restore_context(self, surface, length):
        self.current = self.contexts[0]
        self.contexts.remove(self.contexts[0])

    def __init__(self):
        self.rules = {
            "X" : None,
            "F" : self.draw_forward,
            "-" : self.turn_left,
            "+" : self.turn_right,
            "[" : self.save_context,
            "]" : self.restore_context
        }
        self.contexts = []
        self.current = []

    def draw_forward(self, surface, length):
        dest = [length * math.cos(self.current[2]) + self.current[0], length * math.sin(self.current[2]) + self.current[1]]
        # colors = [0x8B527A]
        color = 0x6033AB # if len(self.contexts) + 1 > len(colors) else colors[len(self.contexts)]
        pygame.draw.line(surface, color, (self.current[0], self.current[1]), dest, 1)
        self.current = [dest[0], dest[1], self.current[2]]

    def generate(self, surface, axiom, n):
        self.current = [400, 700, -3.1415 / 3]
        self.contexts = []
        n_axiom = ""
        for letter in axiom:
            if letter == "F":
                n_axiom += "FF"
            elif letter == "X":
                n_axiom += "F-[[X]+X]+F[+FX]-X"
            else:
                n_axiom += letter
            if n == 0:
                if self.rules[letter] is not None:
                    self.rules[letter](surface, 1)
        if n > 0:
            self.generate(surface, n_axiom, n - 1)
            
def print_degrade(surface, steps, _from, to):
    step = [(-_from[0] + to[0]) / steps, (-_from[1] + to[1]) / steps, (-_from[2] + to[2]) / steps]
    size = (1280, 720 / steps)
    pos = (0, 0)
    b = steps
    while steps:
        color = pygame.Color(_from[0] + step[0], _from[1] + step[1], _from[2] + step[2], 0)
        if steps == 1:
            size = (1280, 150)
        pygame.draw.rect(surface, color, pygame.Rect(pos, size))
        _from[0] = _from[0] + step[0]
        _from[1] = _from[1] + step[1]
        _from[2] = _from[2] + step[2]
        pos = (0, pos[1] + (720 / b))
        steps -= 1

if __name__ == "__main__":
    pygame.init()

    win_size = (width, height) = 1280, 720
    screen = pygame.display.set_mode(win_size)

    plant = Plant()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(1)
            i = 0
            while i < 10:
                print_degrade(screen, 26, [0x05, 0xA9, 0xBF], [0xEC, 0x84, 0x97])
                plant.generate(screen, "X", i)
                pygame.time.wait(500)
                i += 1
                pygame.display.flip()
