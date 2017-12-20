#!/usr/bin/env python
import sys

from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.platypus import Flowable, Table, TableStyle, Spacer, Frame
from reportlab.lib import utils
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait, landscape


class NWDocument :
    def __init__(self, aDocInfo, aStyleSheet, pagesize=A4, orientation="portrait") :
        self.docInfo = aDocInfo
        self.style = aStyleSheet
        self.pagesize = landscape(pagesize) if orientation == "landscape" else portrait(pagesize)

        self.doc = BaseDocTemplate('',
            outputfilepagesize = self.pagesize,
            leftMargin = self.style["marginL"], rightMargin = self.style["marginR"],
            topMargin = self.style["marginT"], bottomMargin = self.style["marginB"])

        portraitTempl = PageTemplate(id="portrait",
            frames=Frame(0, 0, pagesize[0], pagesize[1],
            leftPadding=self.style["marginL"],
            bottomPadding=self.style["marginB"],
            rightPadding=self.style["marginR"],
            topPadding=self.style["marginT"]),
            onPageEnd=self.drawDecoration,
            pagesize=portrait(pagesize))
        self.doc.addPageTemplates(portraitTempl)

        landscapeTempl = PageTemplate(id="landscape",
            frames=Frame(0, 0, pagesize[1], pagesize[0],
            leftPadding=self.style["marginL"],
            bottomPadding=self.style["marginB"],
            rightPadding=self.style["marginR"],
            topPadding=self.style["marginT"]),
            onPageEnd=self.drawDecoration,
            pagesize=landscape(pagesize))
        self.doc.addPageTemplates(landscapeTempl)

        self.setDefaultTemplate(orientation)

        self.decorationItems = []

    def setStyleSheet(self, aStyleSheet) :
        self.style = aStyleSheet

    def addDecoration(self,funcObj):
        self.decorationItems.append(funcObj)

    def build(self,aFileName,content) :
        self.doc.filename = aFileName
        self.doc.build(content)

    def setDefaultTemplate(self, name) :
        for idx, template in enumerate(self.doc.pageTemplates) :
            if template.id == name :
                self.doc._firstPageTemplateIndex = idx
                return


    # Called at the beginning of each page, only used to show progression
    def pageBegins(self, canvas):
        # Printing progression
        # Go to beginning of the line and erase it (does not work on sublime)
        #sys.stdout.write("\r\033[K")

        #sys.stdout.write("%s build, " % ("Temporary" if self.pageCounter.firstRun else "Final"))
        #sys.stdout.write("rendering page " + str(canvas.getPageNumber()) + " of " + (str(self.pageCounter.pageCount) if self.pageCounter.pageCount > 0 else "unknown") + "\n")
        #sys.stdout.flush()
        pass

    def drawDecoration(self, canvas, doc) :
        canvas.saveState()
        self.pageBegins(canvas)

        # Inject page count in documentData as it is needed to render the footer
        #self.documentData["pageCount"] = self.pageCounter.pageCount

        # Call all page drawers
        [drawer(canvas, doc, self.docInfo, self.style) for drawer in self.decorationItems]

        # Release the canvas
        canvas.restoreState()
