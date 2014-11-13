#!/usr/bin/env python2

import entity_manager

class World:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) # to allow user to store data
        self._entities = []
        self._refreshed = []
        self._removed = []
        self.entity_manager = entity_manager.EntityManager(self)
        self.system_manager = system_manager.SystemManager(self)

    def loop_start(self):
        # to actualize refreshed and removed entities
        pass
