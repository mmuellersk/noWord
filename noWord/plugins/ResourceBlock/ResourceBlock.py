#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.lib import colors
from reportlab.lib.units import cm

import noWord.common.utils_rp as cmn_utils_rp

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_fs as cmn_utils_fs


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
        # filename or content element
        if 'filename' in block:
            data = cmn_utils_fs.deserialize(os.path.join(block['_path'], block['filename']))
        elif 'content' in block:
            data = block['content']
        else:
            return []

        # alias element
        alias = block['alias']

        # level element, default 1
        setGlobal = self.getElemValue(block, 'global', False)

        if alias in context.resources:
            context.resources[alias].update(data)
        else:
            context.resources[alias] = data

        if setGlobal:
            context.docInfo.update(data)

        # return empty list
        return []
