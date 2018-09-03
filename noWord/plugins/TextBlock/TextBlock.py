#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph

from noWord.common.PluginInterface import PluginInterface


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

        result = []

        style = context.styleSheet[styleName]
        result.append(context.paragraph(content, style))
        return result
