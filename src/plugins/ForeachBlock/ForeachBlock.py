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

        return self.makeForeach(context, block['_path'], resource, content)

    def makeForeach(self, context, path, resource, subblocks):

        resourceData = context.getResource(context.resources, resource)

        content = []

        index = 0
        for item in resourceData:
            index += 1
            context.textCmdProcessors["current"] = lambda res: context.getResource(
                item, res)
            context.textCmdProcessors["index"] = lambda unused: str(index)

            subcontent = []
            subcontent.extend(context.processFuncObj(subblocks, context, path))

            content.append(subcontent)

        context.textCmdProcessors.pop('current')
        context.textCmdProcessors.pop('index')

        return content
