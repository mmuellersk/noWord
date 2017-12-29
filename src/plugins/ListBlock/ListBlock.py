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

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        items = []

        for item in block["content"]:
            if isinstance(item, list):
                shadowContext = context.clone()
                context.processFuncObj(item, shadowContext)
                shadowContext.process()
                items.append(KeepTogether(
                    shadowContext.paragraphs))
            else:
                items.append(KeepTogether(
                    context.paragraph(item)))

        context.content.append(self.buildListItems(
            context,
            items,
            "numbered" in block and block["numbered"],
            block["start"] if "start" in block else 1))

    def buildListItems(self, context, items, numbered=False, start=1):
        if type(start) is str and start == "continue":
            start = context.lastListCounter

        elif type(start) is not int:
            start = 1

        kwargs = {"bulletDedent": 15,
                  "leftIndent": 30,
                  "spaceAfter": 12,
                  "bulletFontName": context.styleSheet["listBulletFontName"],
                  "start": start}

        if numbered:
            kwargs.update(
                {"bulletFormat": context.styleSheet["listNumberFormat"]})

        else:
            kwargs.update({"value": "bullet",
                           "bulletType":  "bullet",
                           "start": context.styleSheet["listBullet"],
                           "bulletFontSize": 10,
                           "bulletOffsetY": -1})

        context.lastListCounter = start + len(items)

        return ListFlowable([[item, Spacer(1, context.styleSheet["itemsInterSpace"])]
                             for item in items[:-1]] + [items[-1]], **kwargs)
