#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '..')

from reportlab.platypus import CondPageBreak

from common.PluginInterface import PluginInterface
from reportlab.lib.units import cm, mm

import common.utils_rp as cmn_utils_rp


class PDFBlock(PluginInterface):
    def __init__(self):
        self.pages = []

    def Name(self):
        return 'pdf'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        content = []

        # filename element
        pdfFilename = os.path.join(block['_path'], block['filename'])

        # width element
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()

        self.pages = cmn_utils_rp.PDFPages(pdfFilename)

        widths = len(self.pages) * [width]

        for i in range(0, len(self.pages)):
            pdfPage = cmn_utils_rp.PDFPage(self.pages[i], widths[i])
            pdfPage.hAlign = "CENTER"
            content.append(pdfPage)

        return content
