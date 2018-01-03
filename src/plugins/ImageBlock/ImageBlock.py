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
        imageFilename = os.path.join(block['_path'], block['filename'])
        context.appendImage(
            path = imageFilename,
            caption = block['caption'] if 'caption' in block else '',
            width = block['width']*cm,
            align = block['align'].upper() if 'align' in block else 'CENTER',
        )
