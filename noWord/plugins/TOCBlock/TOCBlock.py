#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.platypus import PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from noWord.common.PluginInterface import PluginInterface


class TOCBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'toc'

    def init(self, context):
        # define used styles if not exists already
        if not 'Toc0' in context.styleSheet:
            context.styleSheet['Toc0'] = ParagraphStyle(name="Toc0",
                                                        parent=context.styleSheet['default'],
                                                        alignment=TA_LEFT,
                                                        fontSize=10)

        if not 'Toc1' in context.styleSheet:
            context.styleSheet['Toc1'] = ParagraphStyle(name="Toc1",
                                                        parent=context.styleSheet['default'],
                                                        alignment=TA_LEFT,
                                                        fontSize=10,
                                                        leftIndent=0.5 * cm)

        if not 'Toc2' in context.styleSheet:
            context.styleSheet['Toc2'] = ParagraphStyle(name="Toc2",
                                                        parent=context.styleSheet['default'],
                                                        alignment=TA_LEFT,
                                                        fontSize=10,
                                                        leftIndent=1 * cm)

        if not 'Toc3' in context.styleSheet:
            context.styleSheet['Toc3'] = ParagraphStyle(name="Toc3",
                                                        parent=context.styleSheet['default'],
                                                        alignment=TA_LEFT,
                                                        fontSize=10,
                                                        leftIndent=1.5 * cm)

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        toc = TableOfContents()
        toc.dotsMinLevel = 0
        toc.levelStyles = [
            context.styleSheet["Toc0"],
            context.styleSheet["Toc1"],
            context.styleSheet["Toc2"],
            context.styleSheet["Toc3"]]

        content = []
        content.append(toc)
        content.append(PageBreak())
        return content
