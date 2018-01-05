#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph

from common.PluginInterface import PluginInterface


class TitleBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'title'

    def process(self, block, context):

        # level element, default 1
        level = self.getElemValue(block, 'level', 1)

        # title element, default 'no title'
        title = self.getElemValue(block, 'title', 'No title')

        context.content.append(
            context.paragraph('%s' % title,
                              context.styleSheet['Title%d' % level]))
