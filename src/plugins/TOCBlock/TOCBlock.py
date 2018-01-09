#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.platypus import PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.units import cm

from common.PluginInterface import PluginInterface


class TOCBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'toc'

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
