#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_rp as cmn_utils_rp

from TOCBuilder import TOCBuilder


class ChapterBlock(PluginInterface):
    def __init__(self):
        self.sepChar = '.'

    def Name(self):
        return 'chapter'

    def init(self, context):
        if hasattr(context, 'toc'):
            raise Exception(
                'Chapter plugin failed during init: toc has already been initialized in context by another plugin')

        # this TOC is used for the final construction during processing
        # phase
        context.toc = TOCBuilder()

        # define used styles if not exists already
        if not 'Heading0' in context.styleSheet:
            context.styleSheet['Heading0'] = ParagraphStyle(name="Heading0",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=14,
                                                            spaceBefore=10,
                                                            spaceAfter=8)

        if not 'Heading1' in context.styleSheet:
            context.styleSheet['Heading1'] = ParagraphStyle(name="Heading1",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=12,
                                                            spaceBefore=9,
                                                            spaceAfter=6)

        if not 'Heading2' in context.styleSheet:
            context.styleSheet['Heading2'] = ParagraphStyle(name="Heading2",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=11,
                                                            spaceBefore=8,
                                                            spaceAfter=4)

        if not 'Heading3' in context.styleSheet:
            context.styleSheet['Heading3'] = ParagraphStyle(name="Heading3",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=10,
                                                            spaceBefore=8,
                                                            spaceAfter=4)

    def prepare(self, block, context):

        # title element, default 'no title'
        title = self.getElemValue(block, 'title', 'No title')

        # level element, default 1
        level = self.getElemValue(block, 'level', 0)

        # numbered element, default True
        numbered = self.getElemValue(block, 'numbered', True)

        # label element, default None
        label = self.getElemValue(block, 'label', None)

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

        # label element, default None
        label = self.getElemValue(block, 'label', None)

        return cmn_utils_rp.makeChapter(context, title, level, toc,
                                numbered, self.sepChar, style, label)
