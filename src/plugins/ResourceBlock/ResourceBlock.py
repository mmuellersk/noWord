#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.lib import colors
from reportlab.lib.units import cm

import common.utils_rp as cmn_utils_rp

from common.PluginInterface import PluginInterface
import common.utils_fs as cmn_utils_fs


class ResourceBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'resource'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        # filename element
        filename = block['filename']

        # alias element
        alias = block['alias']

        data = cmn_utils_fs.deserialize(
            os.path.join(block['_path'], filename))

        if alias in context.resources:
            context.resources[alias].update(data)
        else:
            context.resources[alias] = data

        # return empty list
        return []
