#!/usr/bin/env python

import sys
sys.path.insert(0, '..')

from reportlab.platypus import CondPageBreak

from common.PluginInterface import PluginInterface
from reportlab.lib.units import cm, mm


class NewpageBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'newpage'

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        context.content.append(
            CondPageBreak(0.9 * context.doc.currentHeight()))
