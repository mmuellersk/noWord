#!/usr/bin/env python

import sys
sys.path.insert(0, '...')


from reportlab.lib import colors
from reportlab.lib.units import cm

from noWord.common.flowables.Measure import Measure

from noWord.common.PluginInterface import PluginInterface


class MeasureBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'measure'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        measure = Measure()

        content = []
        content.append(measure)

        return content
