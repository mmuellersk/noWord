#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.platypus.flowables import TopPadder

from noWord.common.PluginInterface import PluginInterface

class StickToBottomBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'stickToBottom'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        return [TopPadder(context.processFuncObj(block['content'], context, block['_path'])[0])]
