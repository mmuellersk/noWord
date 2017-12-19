#!/usr/bin/env python

import sys
sys.path.insert(0,'...')

from common.PluginInterface import PluginInterface


class ChapterBlock(PluginInterface) :
    def __init__(self) :
        pass

    def Name(self) :
        return 'chapter'

    def process(self, block) :
        print ('Render title: %s' % block['title'])
