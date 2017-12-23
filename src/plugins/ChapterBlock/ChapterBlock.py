#!/usr/bin/env python

import sys
sys.path.insert(0, '...')


from common.PluginInterface import PluginInterface


class ChapterBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'chapter'

    def process(self, block, context):
        level = 1
        if 'level' in block:
            level = block['level']
        context.content.append(
            context.paragraph('<b>%s</b>' % block['title'],
                              context.styleSheet['Heading%d' % level]))
