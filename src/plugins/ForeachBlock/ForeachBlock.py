#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import KeepTogether

from common.PluginInterface import PluginInterface

import common.utils_rp as cmn_utils_rp


class ForeachBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'foreach'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # resource element
        resource = block['resource']

        # content element
        content = block['content']

        # keys element
        keys = ""

        if "keys" in block:
            keys = block["keys"]

        return self.makeForeach(context, block['_path'], resource, keys, content)

    def makeForeach(self, context, path, resource, keys, subblocks):

        resourceData = context.getResource(context.resources, resource)
        keysData = context.getResource(context.resources, keys)

        content = []

        index = 0
        for item in resourceData:
            if keysData:
                if "id" in item:
                    if item["id"] not in keysData:
                        continue
            
            index += 1
            context.textCmdProcessors["current"] = lambda res: context.getResource(
                item, res)
            context.textCmdProcessors["index"] = lambda unused: str(index)

            subcontent = []
            subcontent.extend(context.processFuncObj(subblocks, context, path))

            content.extend(subcontent)

        if 'current' in context.textCmdProcessors:
            context.textCmdProcessors.pop('current')

        if 'index' in context.textCmdProcessors:
            context.textCmdProcessors.pop('index')

        return content
