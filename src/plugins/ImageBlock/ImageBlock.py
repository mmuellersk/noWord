#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.lib.units import cm

from common.PluginInterface import PluginInterface


class ImageBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'image'

    def process(self, block, context):

        # filename element
        imageFilename = os.path.join(block['_path'], block['filename'])

        # caption element, default ''
        caption = self.getElemValue(block, 'caption', '')

        # width element
        width = block['width'] * cm

        # align element
        align = self.getElemValue(block, 'align', 'CENTER').upper()

        context.appendImage(imageFilename, caption, width, align)
