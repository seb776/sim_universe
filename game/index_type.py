#!/usr/bin/env python2

class _indexType:
    _types = []
    type_id = -1
    def __init__(self):
        global _types
        self.__class__._types.append(self.__class__)
        self.__class__.type_id = len(self.__class__._types) - 1

class IndexType(_indexType):
    def __init__(self):
        if self.__class__.type_id == -1:
            _indexType.__init__(self)
