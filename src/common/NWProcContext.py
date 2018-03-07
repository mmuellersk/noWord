#!/usr/bin/env python
import re
import copy
import sys

from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak
from reportlab.platypus import Spacer, CondPageBreak, KeepTogether, ListFlowable
from reportlab.lib import colors
from reportlab.lib.units import cm

from common.DefaultStyles import styles

import common.utils_di as cmn_utils_di
import common.utils_rp as cmn_utils_rp


class NWProcContext:
    def __init__(self, aDocInfo, aSourcePath, aOutputPath, aPrepareFuncObj, aProcessFuncObj):
        self.docInfo = cmn_utils_di.splitDate(aDocInfo)
        self.sourcePath = aSourcePath
        self.outputPath = aOutputPath

        self.paragraphs = []
        self.styleSheet = styles

        self.resources = {"meta": self.docInfo}
        self.textCmdProcessors = {
            "res": self.resourceProcessor,
            "link": self.processAnchor}

        self.pageCounter = cmn_utils_rp.PageCountBlocker()
        self.dummies = []
        self.currentImage = 1
        self.prepareFuncObj = aPrepareFuncObj
        self.processFuncObj = aProcessFuncObj

        self.anchors = {}

    def buildBegins(self):
        if not self.pageCounter.firstRun:
            for dummy in self.dummies:
                dummy.enable(False)

    # Called at the beginning of each page, only used to show progression
    def pageBegins(self, canvas):
        # Printing progression
        # Go to beginning of the line and erase it (does not work on sublime)
        # sys.stdout.write("\r\033[K")
        sys.stdout.write("%s build, " % (
            "Temporary" if self.pageCounter.firstRun else "Final"))
        sys.stdout.write("rendering page " + str(canvas.getPageNumber()) + " of " + (str(
            self.pageCounter.pageCount) if self.pageCounter.pageCount > 0 else "unknown") + "\n")
        sys.stdout.flush()

    def paragraph(self, text, style=None):
        if style is None:
            style = self.styleSheet["BodyText"]
        p = Paragraph(self.processTextCmds(text), style)
        self.paragraphs.append(p)
        return p

    def getResource(self, source, ref):
        tableRegex = re.compile("^([^\[\]]+)\[(\d+)\]$")
        parts = ref.split("/")
        alias = parts[0]
        path = parts[1:]
        resource = source[alias]
        for child in path:
            result = tableRegex.findall(child)
            if len(result) > 0:
                (key, index) = result[0]
                resource = resource[key][int(index)]
            else:
                resource = resource[child]
        return resource

    def resourceProcessor(self, ref):
        return str(self.getResource(self.resources, ref))

    def processTextCmd(self, cmd, data):
        ret = False
        if cmd not in self.textCmdProcessors:
            print("Unknown text command: " + cmd)
        else:
            ret = self.textCmdProcessors[cmd](data)

        if ret is False:
            return "{{%s:%s}}" % (cmd, data)
        else:
            return ret

    def processTextCmds(self, txt):
        txt = str(txt)
        regex = re.compile("{{(.[a-z]*):(.[a-zA-Z0-9._/\[\]]*)?}}")
        cmds = regex.findall(txt)
        for cmd in cmds:
            txt = txt.replace("{{%s:%s}}" %
                              cmd, self.processTextCmd(cmd[0], cmd[1]))
        return txt

    def process(self):
        # Render document variables
        docStyle = copy.deepcopy(self.styleSheet["templates"])
        if "docStyle" in self.docInfo:
            docStyle.update(self.docInfo["docStyle"])
        for templateKey in docStyle:
            try:
                self.docInfo[templateKey] = docStyle[templateKey].format(
                    **self.docInfo)
            except KeyError:
                self.docInfo[templateKey] = ""

        regex = re.compile("{{(.[a-z]*):(.[a-zA-Z0-9._/\[\]]*)}}")
        txt = ''
        for p in self.paragraphs:
            if isinstance(p, Paragraph):
                txt = p.text
            elif isinstance(p, cmn_utils_rp.TocEntry):
                txt = p._text
            cmds = regex.findall(txt)
            if len(cmds) > 0:
                for cmd in cmds:
                    txt = txt.replace("{{%s:%s}}" %
                                      cmd, self.processTextCmd(cmd[0], cmd[1]))

                if isinstance(p, Paragraph):
                    p.text = txt
                    p.__init__(txt, p.style)

        # Define metadata, not mandatory but cleaner
        metadata = cmn_utils_rp.Metadata(
            *[self.docInfo[template] for template in
                ["documentMetaTitleTemplate",
                 "documentMetaAuthorTemplate",
                 "documentMetaSubjectTemplate",
                 "documentMetaKeywordsTemplate"]],
            creator="noWord - non-WYSIWYG document generator - github.com/mmuellersk/noWord",
            producer="ReportLab PDF Library - www.reportlab.com")

        content = []
        content.append(metadata)
        content.append(self.pageCounter)

        return content

    def processAnchor(self, name):

        if not name in self.anchors:
            print("Warning: anchor not found " + name)
            return ''

        anchor = self.anchors[name]

        return str("<a href=\"#%s\">%s</a>" % (anchor['_name'], anchor['_label']))
