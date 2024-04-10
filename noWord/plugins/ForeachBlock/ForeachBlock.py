#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import KeepTogether

from noWord.common.PluginInterface import PluginInterface

import noWord.common.utils_rp as cmn_utils_rp


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
        resource = context.processTextCmds(block['resource']).strip()

        # content element
        content = block['content']

        # content element
        name = self.getElemValue(block, 'name', 'current')

        keepContentTogether = self.getElemValue(block, 'keeptogether', True)

        # keys element
        keys = None

        if "keys" in block:
            keys = block["keys"]

        return self.makeForeach(context, block['_path'], resource, keys, name, content, keepContentTogether)

    def makeForeach(self, context, path, resource, keys, name, subblocks, keepContentTogether):
        resourceData = context.getResource(context.resources, resource)

        if keys is not None:
            if isinstance(keys, str):
                text = context.processTextCmds(keys)
                if isinstance(text, str):
                    keysData = context.getResource(context.resources, text)
                elif isinstance(text, list):
                    keysData = text
                else:
                    keysData = []
            elif isinstance(keys, list):
                keysData = keys
            else:
                keysData = []
        else:
            keysData = []

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

            if keepContentTogether:
                for index in range(0, len(subcontent)-2):
                    subcontent[index].keepWithNext = True

            content.extend(subcontent)

        if name in context.textCmdProcessors:
            context.textCmdProcessors.pop(name)

        if name+'index' in context.textCmdProcessors:
            context.textCmdProcessors.pop(name+"index")

        if name+"_res" in context.resources:
            context.resources.pop(name+"_res")

        return content
