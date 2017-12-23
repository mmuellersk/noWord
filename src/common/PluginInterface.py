#!/usr/bin/env python


class PluginInterface:
    def __init__(self):
        pass

    def Name(self):
        raise NotImplementedError("Plugin should have a name")

    def Category(self):
        return 'default'

    def process(self, block, context):
        raise NotImplementedError("Plugin should implement process method")
