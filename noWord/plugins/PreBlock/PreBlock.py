#!/usr/bin/env python

import sys
sys.path.insert(0, '...') 

from reportlab.lib.styles import getSampleStyleSheet
from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_rp as cmn_utils_rp


class PreBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'pre'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # content element
        content = block['content']

        pretext = cmn_utils_rp.resolveAllTokensForPre( context, content)
        
        content = []
        content.append(pretext)

        return content
