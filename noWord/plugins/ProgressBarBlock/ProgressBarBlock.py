#!/usr/bin/env python

import sys
sys.path.insert(0, '...')


from reportlab.lib import colors
from reportlab.lib.units import cm

import noWord.common.utils_rp as cmn_utils_rp

from noWord.common.PluginInterface import PluginInterface


class ProgressBarBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'progressbar'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # width element, default currentWidth
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()

        # color element, default black
        color = context.styleSheet[block["color"]
                                   ] if "color" in block else colors.blue

        # height element, default 0.5
        height = self.getElemValue(block, 'height', 0.5)

        # thickness element, default 0.5
        thickness = self.getElemValue(block, 'thickness', 0.5)

        # ratio element, default 0.5
        ratio = float(context.processTextCmds(block["ratio"]))

        progressbar = cmn_utils_rp.ProgressBar(width, height*cm, ratio, color, thickness)

        content = []
        content.append(progressbar)

        return content
