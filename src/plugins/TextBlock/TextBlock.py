#!/usr/bin/env python

import sys
sys.path.insert(0,'...')

from common.PluginInterface import PluginInterface


class TextBlock(PluginInterface) :
    def __init__(self) :
        pass

    def Name(self) :
        return 'text'

    def process(self, block) :
        print ('Render text: %s' % block['content'])
