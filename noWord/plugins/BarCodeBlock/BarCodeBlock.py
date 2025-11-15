#!/usr/bin/env python
import io

from reportlab.platypus import Paragraph
from reportlab.lib.units import cm, mm

from reportlab.graphics.barcode.common import Codabar
from reportlab.graphics.barcode.code128 import Code128
from reportlab.graphics.barcode.qr import QrCode
from reportlab.graphics.barcode.code39 import Standard39


from noWord.common.PluginInterface import PluginInterface


class BarCodeBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'barcode'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        content = []

        # barcode format
        format = self.getElemValue(block, 'format', 'code128')

        # value
        value = context.processTextCmds(block['value']).strip()

        # width element, default currentWidth
        barWidth = self.getElemValue(block, 'barWidth', 0.15)
        
        # height
        barHeight = self.getElemValue(block, 'barHeight', 20)
        
        # border
        border = self.getElemValue(block, 'border', 4)
        
        # human readable
        quiet = self.getElemValue(block, 'quiet', False)

        
        # version (QR Code only)
        version = self.getElemValue(block, 'version', 1)
        
        # human readable
        humanReadable = self.getElemValue(block, 'humanReadable', True)

        barcode = Paragraph("barcode")

        if ( format == 'code128') :
            barcode = Code128( value, 
                                    humanReadable=humanReadable, 
                                    barWidth=barWidth*mm, 
                                    barHeight=barHeight*mm, 
                                    quiet=quiet)
            
        elif (format == 'qr' ) :
            barcode = QrCode(value, 
                             width = barWidth*mm,
                             height = barHeight*mm,
                             qrBorder = border,
                             qrVersion = version)
            
        elif (format == 'codabar' ) :
            barcode = Codabar(value,
                              barWidth=barWidth*mm, 
                              barHeight=barHeight*mm)
        
        elif ( format == 'code39' ) :
            barcode = Standard39(value,
                                 barWidth=barWidth*mm, 
                                 barHeight=barHeight*mm, 
                                 quiet=quiet)
        
        
        content.append( barcode )

        return content