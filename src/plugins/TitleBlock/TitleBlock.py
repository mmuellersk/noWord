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

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        level = 1
        if 'level' in block:
            level = block['level']
        context.content.append(
            context.paragraph('<b>%s</b>' % block['title'],
                              context.styleSheet['Title%d' % level]))
