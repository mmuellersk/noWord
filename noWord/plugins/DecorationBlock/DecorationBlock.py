#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from noWord.common.PluginInterface import PluginInterface
from noWord.common.utils_rp import TriggerFlowable

class DecorationBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'decoration'

    def init(self, context):
        self.defaultDecorations = list(context.doc.enabledDecorations)

    def prepare(self, block, context):
        pass

    def reset(self, doc):
        doc.enabledDecorations = list(self.defaultDecorations)

    def setDecorations(self, doc, enabledDecorations):
        doc.enabledDecorations = [deco for deco in doc.availableDecorations if deco.__name__ in enabledDecorations]

    def process(self, block, context):
        callback = lambda: print("No decoration specified")
        if "default" in block and block["default"]:
            callback = lambda: self.reset(context.doc)
        elif "decorations" in block and type(block["decorations"]) is list:
            callback = lambda: self.setDecorations(context.doc, block["decorations"])
        return [TriggerFlowable(callback)]
