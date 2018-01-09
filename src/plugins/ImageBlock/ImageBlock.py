#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.units import cm

from common.PluginInterface import PluginInterface
import common.utils_rp as cmn_utils_rp


class ImageBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'image'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # filename element
        imageFilename = os.path.join(block['_path'], block['filename'])

        # caption element, default ''
        caption = self.getElemValue(block, 'caption', '')

        # width element
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()

        # align element
        align = self.getElemValue(block, 'align', 'CENTER').upper()

        # padding element, defaukt 10
        padding = self.getElemValue(block, 'padding', 10)

        return self.makeImage(context, imageFilename, caption, width, align, padding)

    def makeImage(self, context, path, caption='', width=None, align='CENTER', padding=10):
        content = []

        if width is None:
            width = 16 * cm

        if len(caption) > 0:
            caption = str(context.currentImage) + ". " + caption
        context.currentImage = context.currentImage + 1

        image = cmn_utils_rp.getImage(path, width, dummy=True)
        context.dummies.append(image)
        imgData = [[image], [context.paragraph(
            caption, context.styleSheet["ImageCaption"])]]
        imgTable = Table(imgData)
        imgTable.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), align),
                                      ('VALIGN', (0, 0), (-1, -1), align),
                                      ('LEFTPADDING', (0, 0), (-1, -1), padding),
                                      ('RIGHTPADDING', (0, 0), (-1, -1), padding),
                                      ('TOPPADDING', (0, 0), (-1, -1), padding),
                                      ('BOTTOMPADDING', (0, 0), (-1, -1), padding)]))
        imgTable.hAlign = align
        content.append(imgTable)

        return content
