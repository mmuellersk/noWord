#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph

from noWord.common.PluginInterface import PluginInterface

import noWord.common.utils_rp as cmn_utils_rp


class TextBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'text'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # style element, default 'BodyText'
        styleName = context.processTextCmds(
            self.getElemValue(block, 'style', 'BodyText'))

        # content element
        content = block['content']

        style = context.styleSheet[styleName]
        text = context.paragraph(content, style)

        if "vertical" in block:
            if block["vertical"] == "true":
                text = cmn_utils_rp.VerticalText(context.paragraph(content, style))
        
        return [text] 
