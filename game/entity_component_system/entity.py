#!/usr/bin/env python2

class Entity:
    def __init__(self):
        self._components = [] # list of typles (component, muted)
        self._free_spaces = []

    def add_component(self, component):
        _id = 0
        return _id

    def remove_component(self, component):
        if type(component) == "int":
            pass
        else:
            pass

    # default time to 0 => component is muted till unmuting
    def mute_component(self, component, time = 0):
        pass

    def unmute_component(self, component):
        pass
