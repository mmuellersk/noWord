#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph, KeepTogether, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import CondPageBreak
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from common.PluginInterface import PluginInterface

from TOCBuilder import TOCBuilder


class ChapterBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'chapter'

    def init(self, context):
        if hasattr(context, 'toc'):
            raise Exception(
                'Chapter plugin failed during init: toc has already been initialized in context by another plugin')

        context.toc = TOCBuilder()

        # define used styles if not exists already
        if not 'Heading0' in context.styleSheet:
            context.styleSheet['Heading0'] = ParagraphStyle(name="Heading0",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=20,
                                                            spaceBefore=10,
                                                            spaceAfter=10)

        if not 'Heading1' in context.styleSheet:
            context.styleSheet['Heading1'] = ParagraphStyle(name="Heading1",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=18,
                                                            spaceBefore=9,
                                                            spaceAfter=9)

        if not 'Heading2' in context.styleSheet:
            context.styleSheet['Heading2'] = ParagraphStyle(name="Heading2",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=16,
                                                            spaceBefore=8,
                                                            spaceAfter=8)

    def prepare(self, block, context):
        pass

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

        return self.makeChapter(context, title, level, toc,
                                numbered, '.', style, label)

    def makeChapter(self, context, text, level, toc, numbered, sepChar, style, label=None):
        content = []

        finalText = text

        if numbered:
            finalText = context.toc.renderChapterCounter(level, sepChar) + \
                sepChar + ' ' + text

        tocEntry = context.toc.createTOCEntry(finalText, level)
        chapter = Paragraph("<a name=\"%s\"/>%s" %
                            (tocEntry._link, finalText), style)
        context.paragraphs.append(tocEntry)
        context.paragraphs.append(chapter)

        result = [CondPageBreak(2 * cm)]
        if toc:
            result.append(tocEntry)

        result.append(chapter)
        result.append(Spacer(1, 12 if level == 0 else 6))
        content.append(KeepTogether(result))

        return content
