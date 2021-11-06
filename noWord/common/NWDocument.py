#!/usr/bin/env python
import sys

from reportlab.platypus import PageTemplate
from reportlab.platypus import Flowable, Table, TableStyle, Spacer, Frame
from reportlab.lib import utils
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, A4, A5, A6, portrait, landscape

from noWord.common.utils_rp import DocTemplateWithToc


class NWDocument:
    def __init__(self, aDocInfo, aStyleSheet):
        self.docInfo = aDocInfo
        self.style = aStyleSheet

        if "pageOrientation" in self.docInfo:
            self.orientation = self.docInfo["pageOrientation"]
        else:
            self.orientation = "portrait"

        if "pageSize" in self.docInfo:
            if self.docInfo["pageSize"] == "A3":
                self.pageSize = A3
            elif self.docInfo["pageSize"] == "A5":
                self.pageSize = A5
            elif self.docInfo["pageSize"] == "A6":
                self.pageSize = A6
            else :
                self.pageSize = A5
        else:
            self.pageSize = A4

        if isinstance(self.pageSize, list):
            if len(self.pageSize) > 1:
                self.pageRect = [self.pageSize[0], self.pageSize[1]]
        else:
            self.pageRect = \
                landscape(self.pageSize) \
                if self.orientation == "landscape" \
                else portrait(self.pageSize)

        self.doc = DocTemplateWithToc('',
                                      outputfilepagesize=self.pageRect,
                                      leftMargin=self.style["marginL"], rightMargin=self.style["marginR"],
                                      topMargin=self.style["marginT"], bottomMargin=self.style["marginB"])

        portraitTempl = PageTemplate(id="portrait",
                                     frames=Frame(0, 0, self.pageRect[0], self.pageRect[1],
                                                  leftPadding=self.style["marginL"],
                                                  bottomPadding=self.style["marginB"],
                                                  rightPadding=self.style["marginR"],
                                                  topPadding=self.style["marginT"]),
                                     onPageEnd=self.drawDecoration,
                                     pagesize=self.pageRect)
        self.doc.addPageTemplates(portraitTempl)

        landscapeTempl = PageTemplate(id="landscape",
                                      frames=Frame(0, 0, self.pageRect[0], self.pageRect[1],
                                                   leftPadding=self.style["marginL"],
                                                   bottomPadding=self.style["marginB"],
                                                   rightPadding=self.style["marginR"],
                                                   topPadding=self.style["marginT"]),
                                      onPageEnd=self.drawDecoration,
                                      pagesize=self.pageRect)
        self.doc.addPageTemplates(landscapeTempl)

        self.doc.setDefaultTemplate(self.orientation)

        self.enabledDecorations = []
        self.availableDecorations = []

        self.enabledTransformations = {}
        self.availableTransformations = {}

    def setStyleSheet(self, aStyleSheet):
        self.style = aStyleSheet

        self.doc = DocTemplateWithToc('',
                                      outputfilepagesize=self.pageRect,
                                      leftMargin=self.style["marginL"], rightMargin=self.style["marginR"],
                                      topMargin=self.style["marginT"], bottomMargin=self.style["marginB"])

        portraitTempl = PageTemplate(id="portrait",
                                     frames=Frame(0, 0, self.pageRect[0], self.pageRect[1],
                                                  leftPadding=self.style["marginL"],
                                                  bottomPadding=self.style["marginB"],
                                                  rightPadding=self.style["marginR"],
                                                  topPadding=self.style["marginT"]),
                                     onPageEnd=self.drawDecoration,
                                     pagesize=self.pageRect)
        self.doc.addPageTemplates(portraitTempl)

        landscapeTempl = PageTemplate(id="landscape",
                                      frames=Frame(0, 0, self.pageRect[0], self.pageRect[1],
                                                   leftPadding=self.style["marginL"],
                                                   bottomPadding=self.style["marginB"],
                                                   rightPadding=self.style["marginR"],
                                                   topPadding=self.style["marginT"]),
                                      onPageEnd=self.drawDecoration,
                                      pagesize=self.pageRect)
        self.doc.addPageTemplates(landscapeTempl)

        self.doc.setDefaultTemplate(self.orientation)

    def addDecoration(self, funcObj, enabled=True):
        self.availableDecorations.append(funcObj)
        if enabled: self.enabledDecorations.append(funcObj)

    def addTransformation(self, funcObj, name):
        self.availableTransformations[name]=funcObj
        self.enabledTransformations[name]=funcObj

    def currentHeight(self):
        return self.pageRect[1] - self.style["marginT"] - self.style["marginB"]

    def currentWidth(self):
        return self.pageRect[0] - self.style["marginL"] - self.style["marginR"]

    def build(self, aFileName, context, content):
        self.context = context
        self.doc.filename = aFileName
        self.doc.multiBuild(content)

    def drawDecoration(self, canvas, doc):
        canvas.saveState()
        self.context.pageBegins(canvas)

        # Inject page count in documentData as it is needed to render the footer
        self.docInfo["pageCount"] = self.context.pageCounter.pageCount

        # Call all page drawers
        [drawer(canvas, doc, self.docInfo, self.style)
         for drawer in self.enabledDecorations]

        # Release the canvas
        canvas.restoreState()
