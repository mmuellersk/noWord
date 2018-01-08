#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Table, TableStyle, KeepTogether, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm, mm

from common.PluginInterface import PluginInterface

import common.utils_rp as cmn_utils_rp

class ListBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'list'

    def prepare(self, block, context):
        items = []

        for item in block["content"]:
            if isinstance(item, list):
                context.prepareFuncObj(item, context, block['_path'])

    def process(self, block, context):

        # numbered element, default False
        numbered = self.getElemValue(block, 'numbered', False)

        # start element, default 1
        start = self.getElemValue(block, 'start', 1)

        # itemspace element, default see styleSheet
        itemSpace = self.getElemValue(block, 'itemspace',
            context.styleSheet["itemsInterSpace"])

        items = []

        for item in block["content"]:
            if isinstance(item, list):
                context.processFuncObj(item, context, block['_path'])
                items.append(KeepTogether(
                    context.process()))
            else:
                items.append(
                    context.paragraph(item))

        return cmn_utils_rp.makeList(context, items, numbered, start, itemSpace)
