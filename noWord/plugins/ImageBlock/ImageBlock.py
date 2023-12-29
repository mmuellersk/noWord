#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_rp as cmn_utils_rp


class ImageBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'image'

    def init(self, context):
        if not 'ImageCaption' in context.styleSheet:
            context.styleSheet['ImageCaption'] = ParagraphStyle(name="ImageCaption",
                                                                parent=context.styleSheet['default'],
                                                                alignment=TA_CENTER,
                                                                fontSize=12,
                                                                spaceBefore=4,
                                                                spaceAfter=8)

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # filename element
        filename = context.processTextCmds(block['filename']).strip()

        imageFilename = os.path.join(block['_path'], filename)

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
            caption = str(context.doc.currentImage) + ". " + caption
        context.currentImage = context.doc.currentImage + 1

        image = cmn_utils_rp.getImage(path, width, dummy=True)
        context.doc.dummies.append(image)
        imgData = [[image], [cmn_utils_rp.resolveAllTokens( context, 
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
