#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph, KeepTogether

from noWord.common.PluginInterface import PluginInterface

import noWord.common.utils_rp as cmn_utils_rp


class AnchorBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'anchor'

    def init(self, context):
        pass

    def prepare(self, block, context):
        anchor = {}

        # name element
        anchor['_name'] = block['name']

        # lable element
        anchor['_label'] = block['label']

        if anchor['_name'] in context.anchors:
            print("Warning: overwriting bookmark " + anchor['_name'])
        context.anchors[anchor['_name']] = anchor

    def process(self, block, context):
        # name element
        name = context.processTextCmds(block['name'])

        # lable element
        label = context.processTextCmds(str(block['label']))

        if not name in context.anchors:
            anchor = {}
            # name element
            anchor['_name'] = name

            # lable element
            anchor['_label'] = label

            context.anchors[name] = anchor

        # lable element
        style = self.getElemValue(block, 'style', 'BodyText')

        visible = self.getElemValue(block, 'visible', True)
        keeptogether = self.getElemValue(block, 'keeptogether', True)

        bookmark = cmn_utils_rp.Bookmark(name)

        if visible:
            if keeptogether:
                return [KeepTogether([bookmark, Paragraph(label, context.styleSheet[style])])]
            else:
                return [bookmark, Paragraph(label, context.styleSheet[style])]
        else:
            return [bookmark]
