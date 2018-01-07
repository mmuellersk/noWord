#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph

from common.PluginInterface import PluginInterface


class TextBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'text'

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # style element, default 'BodyText'
        styleName = self.getElemValue(block, 'style', 'BodyText')

        # content element
        content = block['content']

        style = context.styleSheet[styleName]
        context.content.append(context.paragraph(content, style))
