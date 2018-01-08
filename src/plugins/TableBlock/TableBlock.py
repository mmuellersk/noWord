#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm, mm

from common.PluginInterface import PluginInterface
import common.utils_di as cmn_utils_di
import common.utils_rp as cmn_utils_rp


class TableBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'table'

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # width element, default []
        widths = [w * cm for w in block["widths"]] if "widths" in block else []

        # keys element, default block['header']
        keys = block["keys"] if "keys" in block else block["header"]

        # rows element
        if isinstance(block["rows"], str):
            block["rows"] = context.getResource(block["rows"])
        lines = cmn_utils_di.flattenDicts(block["rows"], keys)

        # displayHeader element
        headers = block["header"] if "displayHeader" not in block or block["displayHeader"] else []

        # repeatRows element, default 0
        repeatRows = self.getElemValue(block, 'repeatRows', 0)

        # border element, default 0.5
        border = self.getElemValue(block, 'border', 0.5)

        # halign element, default CENTER
        halign = self.getElemValue(block, 'halign', 'CENTER')

        cmn_utils_rp.appendTable(context, block['_path'],
                            headers, lines, widths, None,
                            halign, [], repeatRows, border)
