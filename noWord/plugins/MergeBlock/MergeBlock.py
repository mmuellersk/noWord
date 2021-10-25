#!/usr/bin/env python
import sys
from copy import deepcopy
sys.path.insert(0, '...')

from noWord.common.PluginInterface import PluginInterface


class MergeBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'merge'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        alias = block['alias']

        targetResource = {}
        if 'resources' in block:
            if isinstance(block['resources'], list):
                for resourceName in block['resources']:
                    data = context.getResource(context.resources, resourceName)
                    targetResource.update(deepcopy(data))

        context.resources[alias] = targetResource

        return []
