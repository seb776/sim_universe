#!/usr/bin/env python2

class GameInstance:
    def __init__(self):
        self.data = GameData()

    def start(self):

        while True:
            sysPhysix.Process()
            sysGraphix.Process()
            sysKeyboard.Process()
        return True
