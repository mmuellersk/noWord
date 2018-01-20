#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph

from common.PluginInterface import PluginInterface

import common.utils_rp as cmn_utils_rp


class AnchorBlock(PluginInterface):
    def __init__(self):
        self.anchors = {}

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

        if anchor['_name'] in self.anchors:
            print("Warning: overwriting bookmark " + anchor['_name'])
        self.anchors[anchor['_name']] = anchor

        if not 'link' in context.textCmdProcessors:
            context.textCmdProcessors['link'] = self.processAnchor

    def process(self, block, context):

        # name element
        name = block['name']

        # lable element
        label = block['label']


        content = [Paragraph('<a name=\"%s\" />%s' % (name, label),
            context.styleSheet['BodyText'])]

        return content

    def processAnchor(self, name):

        if not name in self.anchors:
            print("Warning: anchor not found " + name)
            return ''

        anchor = self.anchors[name]

        return str("<a href=\"#%s\">%s</a>" % (anchor['_name'], anchor['_label']))




