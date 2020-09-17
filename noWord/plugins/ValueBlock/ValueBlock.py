#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Spacer, Paragraph, PageBreak

import noWord.common.utils_rp as cmn_utils_rp

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_fs as cmn_utils_fs


class ValueBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'value'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        return context.processFuncObj(context.getResource(context.resources, block['resource']), context, block['_path'])
