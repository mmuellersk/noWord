#!/usr/bin/env python
import os
import sys
import platform
import re
import reportlab.lib.enums
import copy
import sys
sys.path.insert(0,'..')

from common.PluginManager import PluginManager
from common.DefaultStyles import styles
from common.NWDocument import NWDocument

import common.utils_fs as cmn_utils_fs
import common.utils_di as cmn_utils_di


class ProcessingContext :
    def __init__(self, aDocInfo, aSourcePath, aOutputPath) :
        self.docInfo = cmn_utils_di.splitDate(aDocInfo)
        self.sourcePath = aSourcePath
        self.outputPath = aOutputPath

        self.content = []
        self.styleSheet = styles

class NWGenerator :
    def __init__(self, aSourcePath, aOutputPath) :
        self.pluginMng = PluginManager()

        self.pluginMng.addPluginFolder(
            os.path.join(os.path.dirname(__file__),
            '../plugins/') )

        self.pluginMng.loadPlugins()

        # Load general prefs
        docInfos = cmn_utils_fs.deserialize(
            os.path.join(aSourcePath,
            "doc_info.yaml"))

        self.context = ProcessingContext(docInfos, aSourcePath, aOutputPath)

    def process(self) :
        for block in self.processFolder(self.context.sourcePath) :
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None :
                plugin.process(block, self.context)
            else :
                print('Plugin not found: %s' % block['type'])

        outputfile = os.path.join(self.context.outputPath, 'test.pdf')
        doc = NWDocument(outputfile)
        doc.build(self.context.content)


    def processFolder(self,path) :
        for item in sorted(os.listdir(path)) :
            itemPath = os.path.join(path, item)

            if os.path.isdir(itemPath) and not item.startswith("."):
                for subitem in self.processFolder(itemPath) :
                    yield subitem
            elif item.endswith(".yaml"):
              parts = cmn_utils_fs.loadYAML(itemPath)

              if type(parts) is not list:
                  continue

              for part in parts:
                if "type" not in part:
                    continue

                yield part
