#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from noWord.common.PluginInterface import PluginInterface
from noWord.common.utils_rp import TriggerFlowable

class DecorationManager(object):
    def __init__(self, decorations):
        self.availableDecorations = list(decorations)
        self.enabledDecorations = []

    def reset(self):
        self.enabledDecorations = [deco.__name__ for deco in self.availableDecorations]

    def setDecorations(self, decorations):
        self.enabledDecorations = list(decorations)

    def __call__(self, canvas, doc, info, style):
        for deco in self.availableDecorations:
            if deco.__name__ in self.enabledDecorations:
                deco(canvas, doc, info, style)

class DecorationBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'decoration'

    def init(self, context):
        self.decoManager = DecorationManager(context.doc.decorationItems)
        context.buildBeginsCallbacks.append(self.decoManager.reset)
        context.doc.decorationItems = [self.decoManager]

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        callback = lambda: print("No decoration specified")
        if "default" in block and block["default"]:
            callback = lambda: self.decoManager.reset()
        elif "decorations" in block and type(block["decorations"]) is list:
            callback = lambda: self.decoManager.setDecorations(block["decorations"])
        return [TriggerFlowable(callback)]
