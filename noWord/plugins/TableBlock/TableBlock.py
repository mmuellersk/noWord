#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_di as cmn_utils_di
import noWord.common.utils_rp as cmn_utils_rp


class TableBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'table'

    def init(self, context):
        pass

    def prepare(self, block, context):
        # keys element, default block['header']
        keys = block["keys"] if "keys" in block else block["header"]

        # rows element
        if isinstance(block["rows"], list):
            lines = cmn_utils_di.flattenDicts(block["rows"], keys)

            for line in lines:
                for col in line:
                    if isinstance(col, list):
                        context.prepareFuncObj(col, context, block['_path'])

    def process(self, block, context):

        # keys element, default block['header']
        keys = block["keys"] if "keys" in block else block["header"]
        if isinstance(keys, str):
            keys = context.getResource(context.resources, keys)

        # rows element
        data = block["rows"]
        if isinstance(data, str):
            data = context.getResource(
                context.resources, block["rows"])

            if "filter" in block:
                filters = context.getResource(
                    context.resources, block["filter"])
                resourceData = data
                data = []
                for item in resourceData:
                    if "id" in item:
                        if item["id"] in filters:
                            data.append(item)

        lines = cmn_utils_di.flattenDicts(data, keys)

        # displayHeader element
        headers = block["header"] if "displayHeader" not in block or block["displayHeader"] else []
        if isinstance(headers, str):
            headers = context.getResource(context.resources, headers)

        # width element, default []
        if not lines:
            nbCols = len(headers)
        else:
            nbCols = max(len(headers), len(lines[0]))

        unit = context.doc.currentWidth() if 'unit' in block and block['unit'] == "percent" else cm

        if "widths" in block:
            widths = block["widths"]

            if isinstance(widths, str):
                widths = context.getResource(context.resources, widths)

            widths = [w * unit for w in widths]
        else:
            widths = nbCols * [context.doc.currentWidth() / nbCols]

        # repeatRows element, default 0
        repeatRows = self.getElemValue(block, 'repeatRows', 0)

        # border element, default 0.5
        border = self.getElemValue(block, 'border', 0.5)

        # halign element, default CENTER
        halign = self.getElemValue(block, 'halign', 'CENTER')

        bgcolor = []
        style = []

        if "bgcolor" in block:
            bgcolor = block["bgcolor"]

        bordercolor = colors.black
        if "bordercolor" in block :
            if block["bordercolor"] in context.styleSheet :
                bordercolor = context.styleSheet[block["bordercolor"]]
            else :
                bordercolor = colors.HexColor(block["bordercolor"])

        if "style" in block:
            style = block["style"]

        return cmn_utils_rp.makeTable(context, block['_path'],
                                      headers, lines, widths, None,
                                      halign, [], repeatRows, border, bgcolor, bordercolor, style)
