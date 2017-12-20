#!/usr/bin/env python
import re

from reportlab.platypus import Paragraph

from common.DefaultStyles import styles

import common.utils_di as cmn_utils_di

class NWProcContext :
    def __init__(self, aDocInfo, aSourcePath, aOutputPath) :
        self.docInfo = cmn_utils_di.splitDate(aDocInfo)
        self.sourcePath = aSourcePath
        self.outputPath = aOutputPath

        self.content = []
        self.paragraphs = []
        self.styleSheet = styles

        self.resources = {"meta": self.docInfo}
        self.textCmdProcessors = {
            "res": self.resourceProcessor}

    def paragraph(self, text, style=None):
        if style is None:
            style = self.style["BodyText"]
        p = Paragraph(text, style)
        self.paragraphs.append(p)
        return p

    def getResource(self, ref):
        tableRegex = re.compile("^([^\[\]]+)\[(\d+)\]$")
        parts = ref.split("/")
        alias = parts[0]
        path = parts[1:]
        resource = self.resources[alias]
        for child in path:
            result = tableRegex.findall(child)
            if len(result) > 0:
                (key, index) = result[0]
                resource = resource[key][int(index)]
            else:
                resource = resource[child]
        return resource

    def resourceProcessor(self, ref):
        return str(self.getResource(ref))

    def processTextCmd(self, cmd, data):
        ret = False
        if cmd not in self.textCmdProcessors:
            print("Unknown text command: " + cmd)
        else: ret = self.textCmdProcessors[cmd](data)

        if ret is False: return "{{%s:%s}}" % (cmd, data)
        else: return ret

    def process(self):
        regex = re.compile("{{(.[a-z]*):(.[a-zA-Z0-9._/\[\]]*)}}")
        for p in self.paragraphs:
          if isinstance(p, Paragraph): txt = p.text
          elif isinstance(p, reportUtils.TocEntry): txt = p._text
          cmds = regex.findall(txt)
          if len(cmds) > 0:
            for cmd in cmds:
              txt = txt.replace("{{%s:%s}}" % cmd, self.processTextCmd(cmd[0], cmd[1]))

            if isinstance(p, Paragraph):
              p.text = txt
              p.__init__(txt, p.style)
