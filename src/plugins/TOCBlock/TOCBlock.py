#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.lib.units import cm

from common.PluginInterface import PluginInterface


class TOCBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'toc'

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        context.appendTOC()
