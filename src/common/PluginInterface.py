#!/usr/bin/env python


class PluginInterface:
    def __init__(self):
        pass

    def Name(self):
        raise NotImplementedError("Plugin should have a name")

    def Category(self):
        return 'default'

    def prepare(self, block, context):
        raise NotImplementedError("Plugin should implement prepare method")

    def process(self, block, context):
        raise NotImplementedError("Plugin should implement process method")

    def getElemValue(self, block, aKey, defaultValue):

        elem = defaultValue

        if aKey in block:
            elem = block[aKey]

        return elem
