#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Table, TableStyle, KeepTogether, ListFlowable, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm, mm

from common.PluginInterface import PluginInterface


class ListBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'list'

    def process(self, block, context):

        # numbered element, default False
        numbered = self.getElemValue(block, 'numbered', False)

        # start element, default 1
        start = self.getElemValue(block, 'start', 1)

        items = []

        for item in block["content"]:
            if isinstance(item, list):
                shadowContext = context.clone()
                context.processFuncObj(item, shadowContext, block['_path'])
                shadowContext.process()
                context.collect(shadowContext)
                items.append(KeepTogether(
                    shadowContext.content))
            else:
                items.append(
                    context.paragraph(item))

        context.content.append(
            self.buildListItems(context, items, numbered, start))

    def buildListItems(self, context, items, numbered=False, start=1):
        if type(start) is str and start == "continue":
            start = context.lastListCounter

        elif type(start) is not int:
            start = 1

        kwargs = {"bulletDedent": 15,
                  "leftIndent": 30,
                  "spaceAfter": 0,
                  "bulletFontName": context.styleSheet["listBulletFontName"],
                  "start": start}

        if numbered:
            kwargs.update(
                {"bulletFormat": context.styleSheet["listNumberFormat"]})

        else:
            kwargs.update({"value": "bullet",
                           "bulletType":  "bullet",
                           "start": context.styleSheet["listBullet"],
                           "bulletFontSize": 8,
                           "bulletOffsetY": -1})

        context.lastListCounter = start + len(items)

        return ListFlowable([[item, Spacer(1, context.styleSheet["itemsInterSpace"])]
                             for item in items[:-1]] + [items[-1]], **kwargs)
