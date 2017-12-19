#!/usr/bin/env python
import os
import sys
import platform
import re
import reportlab.lib.enums
import copy

import common.utils_fs as cmn_utils_fs
import common.utils_di as cmn_utils_di


class NWGenerator :
    def __init__(self, aDocInfo, aSourcePath, aOutputPath) :
        self.docInfo = cmn_utils_di.splitDate(aDocInfo)
        self.sourcePath = aSourcePath
        self.outputPath = aOutputPath

    def process(self) :
        self.processFolder(self.sourcePath)


    def processFolder(self,path) :
        for item in sorted(os.listdir(path)) :
            itemPath = os.path.join(path, item)
            if os.path.isdir(itemPath) and not item.startswith("."):
              self.processFolder(itemPath)
            elif item.endswith(".yaml"):
              parts = cmn_utils_fs.loadYAML(itemPath)
              if type(parts) is not list: continue
              for part in parts:
                if "type" not in part: continue
