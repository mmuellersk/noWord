#!/usr/bin/env python

import sys
sys.path.insert(0,'...')

from reportlab.platypus import Paragraph

from common.PluginInterface import PluginInterface


class ChapterBlock(PluginInterface) :
    def __init__(self) :
        pass

    def Name(self) :
        return 'chapter'

    def process(self, block, context) :
        level = 1
        if 'level' in block :
            level = block['level']
        context.content.append(Paragraph(block['title'],
            context.styleSheet['Heading%d' % level]))

        if 'content' in block :
            context.content.append(Paragraph(block['content'],
                context.styleSheet['BodyText']))
