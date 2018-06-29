#!/usr/bin/env python

import sys
sys.path.insert(0, '...')


from reportlab.lib import colors
from reportlab.lib.units import cm

import common.utils_rp as cmn_utils_rp

from common.PluginInterface import PluginInterface


class LineBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'line'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # dashes element
        dashes = [1, 0]
        if "dashes" in block and type(block["dashes"]) is bool and block["dashes"]:
            dashes = [4, 3]
        elif "dashes" in block and type(block["dashes"]) is list:
            dashes = block["dashes"]

        # width element, default currentWidth
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()

        # color element, default black
        color = context.styleSheet[block["color"]
                                   ] if "color" in block else colors.black

        # thickness element, default 0.5
        thickness = self.getElemValue(block, 'thickness', 0.5)

        # rounded element, default False
        rounded = self.getElemValue(block, 'rounded', False)

        line = cmn_utils_rp.Hline(width, color, thickness, rounded, dashes)

        content = []
        content.append(line)

        return content
