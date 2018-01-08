#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph, KeepTogether, Spacer
from reportlab.platypus import CondPageBreak
from reportlab.lib.units import cm

from common.PluginInterface import PluginInterface

from TOCBuilder import TOCBuilder


class ChapterBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'chapter'

    def prepare(self, block, context):
        if not hasattr(context, 'toc'):
            context.toc = TOCBuilder()

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

        self.appendChapter(context, title, level, toc,
                           numbered, '.', style, label)

    def appendChapter(self, context, text, level, toc, numbered, sepChar, style, label=None):
        finalText = text

        if toc and numbered:
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
        context.content.append(KeepTogether(result))
