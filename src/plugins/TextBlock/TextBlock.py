#!/usr/bin/env python

import sys
sys.path.insert(0,'...')

from reportlab.platypus import Paragraph

from common.PluginInterface import PluginInterface


class TextBlock(PluginInterface) :
    def __init__(self) :
        pass

    def Name(self) :
        return 'text'

    def process(self, block, context) :
        context.content.append(context.paragraph(block['content'],
            context.styleSheet['BodyText']))
