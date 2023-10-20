#!/usr/bin/env python
import re
import copy

from noWord.common.DefaultStyles import styles

import noWord.common.utils_di as cmn_utils_di
import noWord.common.utils_rp as cmn_utils_rp


class NWProcContext:
    def __init__(self, aDocInfo, aSourcePath, aOutputPath, aPrepareFuncObj, aProcessFuncObj):
        self.docInfo = cmn_utils_di.splitDate(aDocInfo)
        self.sourcePath = aSourcePath
        self.outputPath = aOutputPath

        self.styleSheet = styles

        self.resources = {"meta": self.docInfo}
        self.textCmdProcessors = {
            "res": self.resourceProcessor,
            "link": self.processAnchor,
            "ref": self.processRef,
            "titleref": self.processTitleRef,
            "inc": self.processIncrement,
            "incval": self.processIncrementValue,
            "count": self.processCount}
        
        self.prepareFuncObj = aPrepareFuncObj
        self.processFuncObj = aProcessFuncObj

        self.anchors = {}
        self.incs = {}

    def addResource(self, key, value):
        self.resources[key] = value

    def getResource(self, source, ref):
        tableRegex = re.compile("^([^\[\]]+)\[(\d+)\]$")
        parts = ref.split("/")
        alias = parts[0]
        path = parts[1:]
        if alias not in source:
            return None
        resource = source[alias]
        for child in path:
            result = tableRegex.findall(child)
            if len(result) > 0:
                (key, index) = result[0]
                resource = resource[key][int(index)]
            else:
                try:
                    resource = resource[child]
                except:
                    return None
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
        regex = re.compile("{{(.[a-z]*):(.[-a-zA-Z0-9._\/\[\]]*)?}}")

        while True:
            cmds = regex.findall(txt)
            if not len(cmds):
                break

            cmd = cmds[0]

            originalTxt = txt

            textProcessed = self.processTextCmd(cmd[0], cmd[1])

            if isinstance(textProcessed, str):
                txt = txt.replace("{{%s:%s}}" %
                                  cmd, textProcessed)
            elif isinstance(textProcessed, list):
                return textProcessed
            else:
                txt = txt.replace("{{%s:%s}}" %
                                  cmd, str(textProcessed))

            if txt == originalTxt:
                break

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

        return content

    def processAnchor(self, name):

        if not name in self.anchors:
            print("Warning: anchor not found " + name)
            return ''

        anchor = self.anchors[name]

        return str("<a href=\"#%s\">%s</a>" % (anchor['_name'], anchor['_label']))

    def processRef(self, ref):
        if ref not in self.anchors:
            print("Reference " + ref + " not found!")
            return False
        bookmark = self.anchors[ref]
        if "_name" in bookmark: return "<a href=\"#%s\">%s</a>" % (bookmark["_name"], bookmark["_label"])
        else: return bookmark['_label']

    def processTitleRef(self, ref):
        if ref not in self.anchors:
            print("Reference " + ref + " not found!")
            return False
        bookmark = self.anchors[ref]
        if "_name" in bookmark: return "<a href=\"#%s\">%s</a>" % (bookmark["_name"], bookmark["_text"])
        else: return bookmark['_text']

    def processIncrement(self, label):
        if label not in self.incs:
            self.incs[label] = 1
        else:
            self.incs[label] = self.incs[label] + 1

        return str(self.incs[label])

    def processIncrementValue(self, label):
        result = 'not found'
        if label in self.incs:
            result = self.incs[label]

        return str(result)

    def processCount(self, label):
        result=-1;
        listres = self.getResource(
            self.resources, label)
        if label:
            result = len(listres)
        else:
            print('Resource not found')

        return str(result)
