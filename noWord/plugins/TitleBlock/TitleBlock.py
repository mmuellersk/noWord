#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_rp as cmn_utils_rp


class TitleBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'title'

    def init(self, context):
        if not 'Title0' in context.styleSheet:
            context.styleSheet['Title0'] = ParagraphStyle(name="Title0",
                                                          parent=context.styleSheet['default'],
                                                          alignment=TA_LEFT,
                                                          fontSize=18,
                                                          spaceBefore=16,
                                                          spaceAfter=24)

        if not 'Title1' in context.styleSheet:
            context.styleSheet['Title1'] = ParagraphStyle(name="Title1",
                                                          parent=context.styleSheet['default'],
                                                          alignment=TA_LEFT,
                                                          fontSize=16,
                                                          spaceBefore=10,
                                                          spaceAfter=18)

        if not 'Title2' in context.styleSheet:
            context.styleSheet['Title2'] = ParagraphStyle(name="Title2",
                                                          parent=context.styleSheet['default'],
                                                          alignment=TA_LEFT,
                                                          fontSize=14,
                                                          spaceBefore=10,
                                                          spaceAfter=16)

        if not 'Title3' in context.styleSheet:
            context.styleSheet['Title3'] = ParagraphStyle(name="Title3",
                                                          parent=context.styleSheet['default'],
                                                          alignment=TA_LEFT,
                                                          fontSize=12,
                                                          spaceBefore=10,
                                                          spaceAfter=14)

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # level element, default 1
        level = self.getElemValue(block, 'level', 1)

        # title element, default 'no title'
        title = self.getElemValue(block, 'title', 'No title')

        content = []
        content.append(
            cmn_utils_rp.resolveAllTokens( context,'%s' % title,
                              context.styleSheet['Title%d' % level]))
        return content
