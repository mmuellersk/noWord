#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Spacer

from common.PluginInterface import PluginInterface
from reportlab.lib.units import cm, mm


class VSpaceBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'vspace'

    def process(self, block, context):

        # height element, default 12
        height = block["height"] * cm if "height" in block else 12

        context.content.append(Spacer(1, height))
