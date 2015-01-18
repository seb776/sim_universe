#!/usr/bin/env python2

class World:
    def __init__(self):
        self.entity_manager = EntityManager()
        self.system_manager = SystemManager()
        self.group_manager = GroupManager()
        self.tag_manager = TagManager()
