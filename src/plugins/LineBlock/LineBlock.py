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

    def process(self, block, context):
        dashes = [1, 0]
        if "dashes" in block and type(block["dashes"]) is bool and block["dashes"]:
            dashes = [4, 3]
        elif "dashes" in block and type(block["dashes"]) is list:
            dashes = block["dashes"]
        line = cmn_utils_rp.Hline(
            width=block["width"] * cm if "width" in block else context.doc.currentWidth(),
            color=context.styleSheet[block["color"]] if "color" in block else colors.black,
            thickness=block["thickness"] if "thickness" in block else 0.5,
            rounded=block["rounded"] if "rounded" in block else False,
            dashes=dashes)
        if "align" in block:
            line.hAlign = block["align"].upper()

        context.content.append(line)
