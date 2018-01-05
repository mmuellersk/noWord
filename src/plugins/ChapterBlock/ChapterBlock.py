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

        # level element, default 1
        level = self.getElemValue(block, 'level', 1)

        # title element, default 'no title'
        title = self.getElemValue(block, 'title', 'No title')

        context.content.append(
            context.paragraph('%s' % title,
                              context.styleSheet['Heading%d' % level]))
