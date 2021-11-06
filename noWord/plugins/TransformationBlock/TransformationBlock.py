#!/usr/bin/env python
import os
import sys
import glob
sys.path.insert(0, '...')



import noWord.common.utils_rp as cmn_utils_rp
import noWord.common.utils_di as cmn_utils_di

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_fs as cmn_utils_fs


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
