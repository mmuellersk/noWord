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

        # content element
        name = self.getElemValue(block, 'name', 'current')

        # keys element
        keys = ""

        if "keys" in block:
            keys = block["keys"]

        return self.makeForeach(context, block['_path'], resource, keys, name, content)

    def makeForeach(self, context, path, resource, keys, name, subblocks):

        resourceData = context.getResource(context.resources, resource)

        keysData = None
        if keys in context.resources:
            keysData = context.getResource(context.resources, keys)

        content = []

        index = 0
        for item in resourceData:
            if keysData:
                if "id" in item:
                    if item["id"] not in keysData:
                        continue

            index += 1
            context.textCmdProcessors[name] = lambda res: context.getResource(
                item, res)
            context.textCmdProcessors[name+"index"] = lambda unused: str(index)

            context.resources[name+"_res"] = item

            subcontent = []
            subcontent.extend(context.processFuncObj(subblocks, context, path))

            content.extend(subcontent)

        if name in context.textCmdProcessors:
            context.textCmdProcessors.pop(name)

        if name+'index' in context.textCmdProcessors:
            context.textCmdProcessors.pop(name+"index")

        if name+"_res" in context.resources:
            context.resources.pop(name+"_res")

        return content
