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
        level = self.getElemValue(block, 'level', 0)
        style = context.styleSheet['Heading%d' % level]

        # title element, default 'no title'
        title = self.getElemValue(block, 'title', 'No title')

        # toc element, default True
        toc = self.getElemValue(block, 'toc', True)

        # numbered element, default True
        numbered = self.getElemValue(block, 'numbered', True)

        # lebel element, default None
        label = self.getElemValue(block, 'label', None)

        context.appendChapter(title, level, toc, numbered, '.', style, label)
