#!/usr/bin/env python2

class Component:
    def __init__(self, _id):
        self._id = _id

def resize(l, new_size, filling=None):
    if len(l) >=

class Entity:
    def __init__(self):
        self._muted = []
        self._components_by_type = [] # list of tuples (component, muted)

    def add_component(self, component):
        _id = 0
        if len(self._free_spaces) > 0:
            _id = self._free_spaces[0]
            self._free_spaces.remove(self._free_spaces[0])
            self._components[_id] = (-1, component)
        else:
            self._components.append(component)
            _id = len(self._components - 1)
        return _id

    def remove_component(self, component):
        self._free_spaces.insert(0, component._id)
        self._components[component._id] = None

    # default time to 0 => component is muted till unmuting
    def mute_component(self, component, time = 0):
        self._components[component._id] = (time, component)

    def unmute_component(self, component):
        self._components[component._id] = (-1, component)        
