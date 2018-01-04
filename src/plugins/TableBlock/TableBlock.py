#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm, mm

from common.PluginInterface import PluginInterface


class TableBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'table'

    def process(self, block, context):
        widths = [w * cm for w in block["widths"]] if "widths" in block else []
        if isinstance(block["rows"], str):
            block["rows"] = context.getResource(block["rows"])

        keys = block["keys"] if "keys" in block else block["header"]

        context.content.append(
            self.buildTable(context, block['_path'],
                            headers=block["header"] if "displayHeader" not in block or block["displayHeader"] else [
            ],
                lines=self.flattenDicts(block["rows"], keys),
                widths=widths,
                repeatRows=block["repeatRows"] if "repeatRows" in block else 0,
                border=block["border"] if "border" in block else 0.5))

    def flattenDicts(self, dictList, keys=[]):
        if len(dictList) == 0:
            return []
        if len(keys) == 0:
            keys = dictList[0].keys()
        return [[d[k] for k in keys] for d in dictList]

    def buildTable(self, context, path, headers, lines, widths=[],
                   heights=None, halign="CENTER", highlights=[],
                   repeatRows=0, border=0.5):
        # It is possible to render a table without headers
        nbCols = max(len(headers), len(lines[0]))
        nbLines = len(lines) + 1 if len(headers) > 0 else 0

        tableData = []
        headersLine = []
        style = [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                 ('VALIGN', (0, 0), (-1, -1), 'TOP')]
        if border > 0:
            style.append(('GRID', (0, 0), (-1, -1), border, colors.black))

        for col in headers:
            headersLine.append(
                context.paragraph("<b>" + col + "</b>", context.styleSheet["BodyText"]))
        if len(headers) > 0:
            tableData.append(headersLine)
            style.append(("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey))

        for lineNumber in highlights:
            lineNumber = lineNumber + 1 if len(headersLine) > 0 else 0
            style.append(("BACKGROUND", (0, lineNumber), (-1, lineNumber),
                          context.styleSheet["highlight"]))

        for line in lines:
            lineData = []
            for col in line:
                if isinstance(col, str):
                    lineData.append(
                        context.paragraph(col, context.styleSheet["BodyText"]))
                elif isinstance(col, list):
                    shadowContext = context.clone()
                    context.processFuncObj(col, shadowContext, path)
                    shadowContext.process()
                    context.collect(shadowContext)
                    lineData.append(shadowContext.content)

            tableData.append(lineData)

        # if len(widths) == 0:
        #  widths = nbCols*[self.currentWidth() / nbCols]

        table = Table(tableData, widths, heights, repeatRows=repeatRows)
        table.setStyle(TableStyle(style))
        table.hAlign = halign

        return table
