#!/usr/bin/env python
import os
import sys
import glob
sys.path.insert(0, '...')


from noWord.common.PluginInterface import PluginInterface


class TransformationBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'transformation'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        input = block["input"]
        outputName = block['output']

        transfo = block['transformation']
        params = block['params']

        if transfo in context.doc.enabledTransformations :

            outputRes = context.doc.enabledTransformations[transfo](input, params, context)
            context.resources[outputName] = outputRes


        # return empty list
        return []
