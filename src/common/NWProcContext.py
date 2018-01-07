#!/usr/bin/env python
import re
import copy
import sys

from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.units import cm

from common.DefaultStyles import styles

import common.NWTOCContext as NWTOCContext

import common.utils_di as cmn_utils_di
import common.utils_rp as cmn_utils_rp


class NWProcContext:
    def __init__(self, aDocInfo, aSourcePath, aOutputPath, aProcessFuncObj):
        self.docInfo = cmn_utils_di.splitDate(aDocInfo)
        self.sourcePath = aSourcePath
        self.outputPath = aOutputPath

        self.content = []
        self.content.append(cmn_utils_rp.TriggerFlowable(self.buildBegins))
        self.paragraphs = []
        self.styleSheet = styles

        self.resources = {"meta": self.docInfo}
        self.textCmdProcessors = {
            "res": self.resourceProcessor}

        self.pageCounter = cmn_utils_rp.PageCountBlocker()
        self.dummies = []
        self.currentImage = 1
        self.processFuncObj = aProcessFuncObj

        self.lastListCounter = 1

        self.toc = NWTOCContext()

    def clone(self):
        cloneContext = NWProcContext(
            self.docInfo,
            self.sourcePath,
            self.outputPath,
            self.processFuncObj)

        cloneContext.doc = self.doc

        # pass stylesheet in case if it was overriden
        cloneContext.styleSheet = self.styleSheet

        return cloneContext

    def collect(self, otherContext):
        self.dummies.extend(otherContext.dummies)

    def buildBegins(self):
        if not self.pageCounter.firstRun:
            for dummy in self.dummies:
                dummy.enable(False)

    def appendChapter(self, text, level, toc, numbered, sepChar, style, label=None):
        finalText = text

        if toc and numbered:
            finalText = self.toc.renderChapterCounter(level,sepChar) +
                sepChar + text

        tocEntry = self.toc..createTOCEntry(text, level)
        block = Paragraph("<a name=\"%s\"/><b>%s</b>" % (tocEntry._link, text), style)
        self.paragraphs.append(tocEntry)
        self.paragraphs.append(block)

    def appendImage(self, path, caption='', width=None, align='CENTER'):
        if width is None:
            width = 16 * cm

        if len(caption) > 0:
            caption = str(self.currentImage) + ". " + caption
            self.currentImage = self.currentImage + 1

        image = cmn_utils_rp.getImage(path, width, dummy=True)
        self.dummies.append(image)
        imgData = [[image], [self.paragraph(
            caption, self.styleSheet["ImageCaption"])]]
        imgTable = Table(imgData)
        imgTable.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), align),
                                      ('VALIGN', (0, 0), (-1, -1), align),
                                      ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                      ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                                      ('TOPPADDING', (0, 0), (-1, -1), 0),
                                      ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
        imgTable.hAlign = align
        self.content.append(imgTable)

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
        else:
            ret = self.textCmdProcessors[cmd](data)

        if ret is False:
            return "{{%s:%s}}" % (cmd, data)
        else:
            return ret

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
        for p in self.paragraphs:
            if isinstance(p, Paragraph):
                txt = p.text
            # elif isinstance(p, reportUtils.TocEntry):
            #    txt = p._text
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
            creator="noWord - non-WYSIWYG document generator",
            producer="ReportLab PDF Library - www.reportlab.com")

        self.content.append(metadata)
        self.content.append(self.pageCounter)
