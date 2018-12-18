#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '..')

from reportlab.platypus import CondPageBreak

from noWord.common.PluginInterface import PluginInterface
from reportlab.lib.units import cm, mm

import noWord.common.utils_rp as cmn_utils_rp


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
        rawPdfFilename = os.path.join(block['_path'], block['filename'])

        pdfFilename = context.processTextCmds(rawPdfFilename)

        # width element
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()

        self.pages = cmn_utils_rp.PDFPages(pdfFilename)

        # Range
        indices = self.getElemValue(block, "range", [1, len(self.pages)])
        if len(indices) < 2: indices.append(len(self.pages))

        # Border
        border = self.getElemValue(block, "border", 0)

        # Offsets
        xoffset = self.getElemValue(block, "xoffset", 0)*cm
        yoffset = self.getElemValue(block, "yoffset", 0)*cm

        for i in range(indices[0] - 1, indices[1]):
            pdfPage = cmn_utils_rp.PDFPage(self.pages[i], width, border, xoffset, yoffset)
            pdfPage.hAlign = "CENTER"
            content.append(pdfPage)

        return content
