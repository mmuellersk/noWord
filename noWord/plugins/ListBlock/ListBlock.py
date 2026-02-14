#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Table, TableStyle, KeepTogether, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm, mm

from noWord.common.PluginInterface import PluginInterface

import noWord.common.utils_rp as cmn_utils_rp


class ListBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'list'

    def init(self, context):
        context.lastListCounter = 1

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
        if 'start' in block:
            if (type(block['start']) is str) and (start == "continue"):
                start = context.lastListCounter

        # itemspace element, default see styleSheet
        itemSpace = self.getElemValue(block, 'itemspace',
                                      context.styleSheet["itemsInterSpace"])

        # style element, default 'BodyText'
        styleName = self.getElemValue(block, 'style', 'BodyText')
        style = context.styleSheet[styleName]

        items = []

        if isinstance(block["content"], list):
            for item in block["content"]:
                if isinstance(item, list):
                    content = []
                    content.extend(context.processFuncObj(
                        item, context, block['_path']))
                    items.append(KeepTogether(content))
                else:
                    items.append(
                        cmn_utils_rp.resolveAllTokens( context, item, style))
        elif isinstance(block["content"], str):
            resourceData = context.getResource(
                context.resources, block["content"])
            for item in resourceData:
                items.append(
                    cmn_utils_rp.resolveAllTokens( context, item, style))

        return cmn_utils_rp.makeList(context, items, numbered, start, itemSpace)
