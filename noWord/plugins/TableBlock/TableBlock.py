#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm, mm

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

        # rows element
        data = block["rows"]
        if isinstance(data, str):
            data = context.getResource(
                context.resources, block["rows"])

            if "filter" in block:
                filters = context.getResource(
                    context.resources, block["filter"])
                resourceData = block["rows"]
                block["rows"] = []
                for item in resourceData:
                    if "id" in item:
                        if item["id"] in filters:
                            block["rows"].append(item)

        if block['rows'] is None:
            block['rows'] = ''

        lines = cmn_utils_di.flattenDicts(data, keys)

        # displayHeader element
        headers = block["header"] if "displayHeader" not in block or block["displayHeader"] else []

        # width element, default []
        if not lines:
            nbCols = len(headers)
        else:
            nbCols = max(len(headers), len(lines[0]))

        if "widths" in block:
            widths = [w * cm for w in block["widths"]]
        else:
            widths = nbCols * [context.doc.currentWidth() / nbCols]

        # percent element, default []
        unit = context.doc.currentWidth() if 'unit' in block and block['unit'] == "percent" else cm
        widths = [w*unit for w in block["widths"]] if "widths" in block else []

        # repeatRows element, default 0
        repeatRows = self.getElemValue(block, 'repeatRows', 0)

        # border element, default 0.5
        border = self.getElemValue(block, 'border', 0.5)

        # halign element, default CENTER
        halign = self.getElemValue(block, 'halign', 'CENTER')

        bgcolor = []

        if "bgcolor" in block:
            bgcolor = block["bgcolor"]

        return cmn_utils_rp.makeTable(context, block['_path'],
                                      headers, lines, widths, None,
                                      halign, [], repeatRows, border, bgcolor)
