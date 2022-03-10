import os
import re
import mimetypes as mime
from hashlib import sha1

from reportlab.platypus import Flowable, BaseDocTemplate, Image, Spacer
from reportlab.platypus import ListFlowable, Table, TableStyle
from reportlab.lib import utils, colors
from reportlab.lib.units import cm, mm

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

import noWord.common as cmn

allowedImages = [
    "image/jpeg",
    "image/png",
    "image/x-ms-bmp",
    "image/tiff",
    "image/gif"]

def makeList(context, items, numbered=False, start=1, itemSpace=6):
    kwargs = {"bulletDedent": 15,
              "leftIndent": 30,
              "spaceBefore": 0,
              "spaceAfter": 0,
              "bulletFontName": context.styleSheet["listBulletFontName"],
              "bulletFontSize": context.styleSheet["listBulletFontSize"],
              "start": start}

    if numbered:
        kwargs.update(
            {"bulletFormat": context.styleSheet["listNumberFormat"]})

    else:
        kwargs.update({"value": "bullet",
                       "bulletType":  "bullet",
                       "start": context.styleSheet["listBullet"],
                       "bulletFontSize": 8,
                       "bulletOffsetY": -1})

    context.lastListCounter = start + len(items)

    content = []
    content.append(ListFlowable([[item, Spacer(1, itemSpace)]
                                 for item in items[:-1]] + [items[-1]], **kwargs))

    return content


def makeTable(context, path, headers, lines, widths=[],
              heights=None, halign="CENTER", highlights=[],
              repeatRows=0, border=0.5, bgcolor=[], bordercolor=colors.black, customStyle=[]):

    # If no lines and no header
    if not lines and not headers :
        return[]

    # It is possible to render a table without headers
    if not lines:
        nbCols = len(headers)
    else:
        nbCols = max(len(headers), len(lines[0]))

    nbLines = len(lines) + 1 if len(headers) > 0 else 0

    tableData = []
    headersLine = []
    style = [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
             ('VALIGN', (0, 0), (-1, -1), 'TOP')]

    if border > 0:
        style.append(('GRID', (0, 0), (-1, -1), border, bordercolor))

    for col in headers:
        headersLine.append(
            context.paragraph("<b>" + col + "</b>", context.styleSheet["BodyText"]))
    if len(headers) > 0:
        tableData.append(headersLine)
        style.append(("BACKGROUND", (0, 0), (-1, 0),
                      context.styleSheet["headerBackground"]))

    for lineNumber in highlights:
        lineNumber = lineNumber + 1 if len(headersLine) > 0 else 0
        style.append(("BACKGROUND", (0, lineNumber), (-1, lineNumber),
                      context.styleSheet["highlightBackground"]))

    for item in bgcolor:
        style.append(("BACKGROUND",
                      (item["from"][0], item["from"][1]),
                      (item["to"][0], item["to"][1]),
                      item["color"]))

    if len(customStyle) > 0:
        style = customStyle

    for line in lines:
        lineData = []
        for col in line:
            if isinstance(col, list):
                content = []
                content.extend(context.processFuncObj(col, context, path))
                lineData.append(content)
            else:
                lineData.append(
                    context.paragraph(col, context.styleSheet["BodyText"]))

        tableData.append(lineData)

    table = Table(tableData, widths, heights, repeatRows=repeatRows)
    table.setStyle(TableStyle(style))
    table.hAlign = halign

    content = []
    content.append(table)
    return content


def getImage(filename, width, dummy=False):
    filename = os.path.normpath(filename)

    # The module only uses the file extension, it would be better to use python-magic but
    # this requires to install yet another module with pip. So this is sufficient for now.
    imageType = mime.guess_type(filename)[0]

    if imageType in allowedImages:
        orig = utils.ImageReader(filename)
        iw, ih = orig.getSize()
        aspect = ih / float(iw)
        height = width * aspect
        img = Image(filename, width=width, height=height)

    # Allow to insert a PDF page as an image, just like LaTeX does, this allows to insert
    # vector graphics.
    elif imageType == "application/pdf":
        img = PDFSinglePage(filename, width=width, index=0)
        height = img.height

    else:
        print("Unsupported image type " + imageType + " for " + filename)
        img = Spacer(width, width / 2)
        height = img.width / 2

    return DummyFlowable(Spacer(width, height), img, dummy)


def optimalWidth(par, maxWidth, maxHeight):
    w, minHeight = par.wrap(maxWidth, maxHeight)
    totalMM = int(w / mm)

    while totalMM > 0:
        totalMM -= 1
        w, h = par.wrap(totalMM * mm, maxHeight)
        if h > minHeight:
            totalMM += 1
            break

    return totalMM * mm

# This class provides a proxy that forwards all reportlab calls to a temporary or a final
# embedded flowable, depending on its state. This allows to insert a temporary object and
# define it later. It is mainly used to speed the generation process by not inserting the
# real images in intermediary builds.


class DummyFlowable(Flowable):
    def __init__(self, temp=Spacer(1, 1), final=Spacer(1, 1), enabled=True):
        Flowable.__init__(self)
        self.temp = temp
        self.final = final
        self.enable(enabled)

    def enable(self, enabled): self.current = self.temp if enabled else self.final

    def wrap(self, *args, **kwargs): return self.current.wrap(*args, **kwargs)

    def self(self): return self.current.wrap()

    def identify(self, *args, **
                 kwargs): return self.current.identify(*args, **kwargs)

    def drawOn(self, *args, **kwargs): return self.current.drawOn(*args, **kwargs)

    def wrapOn(self, *args, **kwargs): return self.current.wrapOn(*args, **kwargs)

    def splitOn(self, *args, **
                kwargs): return self.current.splitOn(*args, **kwargs)

    def split(self, *args, **kwargs): return self.current.split(*args, **kwargs)

    def minWidth(self): return self.current.minWidth()

    def getKeepWithNext(self): return self.current.getKeepWithNext()

    def getSpaceAfter(self): return self.current.getSpaceAfter()

    def getSpaceBefore(self): return self.current.getSpaceBefore()

    def isIndexing(self): return self.current.isIndexing()

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'DummyFlowable'
        str += 'temp: %s,\n' % self.temp.__class__
        str += 'final: %s,\n' % self.final.__class__
        str += ') noWord.#%s ' % 'DummyFlowable'

        return str

# Open a PDF file and return an array of xobjects


def PDFPages(filename):
    pages = PdfReader(filename).pages
    return [pagexobj(x) for x in pages]


def PDFSinglePage(filename, width, index):
    pages = PdfReader(filename).pages
    return PDFPage(pagexobj(pages[index]), width)

# Wrap a PDF page (xobject) as a reportlab flowable


class PDFPage(Flowable):
    def __init__(self, page, width, border=0, xoffset=0, yoffset=0):
        self.page = page
        self.width = width
        self.height = width / (page.BBox[2] / page.BBox[3])
        self.border = border
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.overflowX = False
        self.overflowY = False

    def wrap(self, availWidth, availHeight):
        frame = self._doctemplateAttr("frame")

        if frame is not None:
            self.overflowX = self.width > frame._aW
            self.overflowY = self.height > frame._aH
            return (frame._aW, min(frame._aH, self.height))
        return (min(self.width, availWidth), self.height)

    def draw(self):
        factor = 1 / (self.page.BBox[2] / self.width)

        # Handle drawing position manually when the pdf overflows
        x, y = self.canv.absolutePosition(0, 0)
        if self.overflowX or self.overflowY:
            x = (self.canv._pagesize[0] - self.width) / 2
        if self.overflowY:
            y = (self.canv._pagesize[1] - self.height) / 2
        x += self.xoffset
        y += self.yoffset

        # Use the canvas in absolute coordinates
        self.canv.saveState()
        self.canv.resetTransforms()
        self.canv.translate(x, y)
        self.canv.scale(factor, factor)
        self.canv.doForm(makerl(self.canv, self.page))
        self.canv.restoreState()

        # Draw border if any
        if self.border > 0:
            self.canv.saveState()
            self.canv.resetTransforms()
            self.canv.setLineWidth(self.border)
            self.canv.setStrokeColor(colors.black)
            self.canv.rect(x, y, self.width, factor*self.page.BBox[3], 1, 0)
            self.canv.restoreState()

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'PDFPage'
        str += 'width: %s,\n' % self.width
        str += 'height: %s,\n' % self.height
        str += ') noWord.#%s ' % 'PDFPage'

        return str

# This empty flowable is provides a trigger that will call a function when it is rendered.


class TriggerFlowable(Flowable):
    def __init__(self, drawCallback=None, afterPreviousCallback=None):
        Flowable.__init__(self)
        self.drawCallback = drawCallback
        self.afterPreviousCallback = afterPreviousCallback

    def draw(self):
        if self.drawCallback is not None: self.drawCallback()

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'TriggerFlowable'
        str += 'callback: %s,\n' % self.callback.__name__
        str += ') noWord.#%s ' % 'TriggerFlowable'
        return str

# This flowable creates a table of content entry where it is placed.


class TocEntry(Flowable):
    def __init__(self, level, text, link):
        self._level = level
        self._text = text
        self._link = link
        self.width = 0
        self.height = 0

    def draw(unused):
        return

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'TocEntry'
        str += '_level: %s,\n' % self._level
        str += '_text: %s,\n' % self._text
        str += '_link: %s,\n' % self._link
        str += 'width: %s,\n' % self.width
        str += 'height: %s,\n' % self.height
        str += ') noWord.#%s ' % 'TocEntry'

        return str

# Doc Template with table of contents


class DocTemplateWithToc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        self.afterFlowableCallbacks = []

    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'TocEntry':
            level = flowable._level
            text = flowable._text
            link = flowable._link
            self.notify('TOCEntry', (level, text, self.page, link))
            self.canv.bookmarkPage(link)
            self.canv.addOutlineEntry(re.sub("<[^>]*>", "", text), link, level)

        for callback in self.afterFlowableCallbacks:
            callback(self)
        self.afterFlowableCallbacks = []

    def filterFlowables(self, flowables):
        followingFlowable = flowables[1] if len(flowables) > 1 else None
        if isinstance(followingFlowable, TriggerFlowable) and followingFlowable.afterPreviousCallback:
            self.afterFlowableCallbacks.append(followingFlowable.afterPreviousCallback)
        elif isinstance(followingFlowable, Layout) and followingFlowable.stickToPrevious:
            self.afterFlowableCallbacks.append(lambda doc: followingFlowable.changeLayout())

    def setDefaultTemplate(self, name):
        for idx, template in enumerate(self.pageTemplates):
            if template.id == name:
                self._firstPageTemplateIndex = idx
                return

# This class is a trick to define ALL pdf metadata. Some are settable from the docTemplate
# like author, subject etc, but creator and producer would always be set to the default
# "ReportLab PDF Library - www.reportlab.com" string.


class Metadata(Flowable):
    def __init__(self, title="", author="", subject="", keywords="", creator="", producer=""):
        Flowable.__init__(self)
        self.title = title
        self.author = author
        self.subject = subject
        self.keywords = keywords
        self.creator = creator
        self.producer = producer

    def draw(self):
        infos = self.canv._doc.info
        infos.title = self.title
        infos.author = self.author
        infos.subject = self.subject
        infos.keywords = self.keywords
        infos.creator = self.creator
        infos.producer = self.producer
        return

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'Metadata'
        str += 'title: %s,\n' % self.title
        str += 'author: %s,\n' % self.author
        str += 'subject: %s,\n' % self.subject
        str += 'keywords: %s,\n' % self.keywords
        str += 'creator: %s,\n' % self.creator
        str += 'producer: %s\n' % self.producer
        str += ') noWord.#%s ' % 'Metadata'
        return str

# This empty flowable inserts a bookmark in the canvas at its position, it is intended to
# be used in conjunction with a KeepTogether flowable to ensure that the bookmark will be
# inserted at the same position than the target flowable.


class Bookmark(Flowable):
  def __init__(self, name=None):
    Flowable.__init__(self)
    if name is None:
      cmn.currentLink += 1
      name = sha1(str(cmn.currentLink).encode("utf-8")).hexdigest()
    self.link = name

  def draw(self):
    self.canv.bookmarkPage(self.link)
    return



# This class is a trick to count the total number of pages. This class must be included at
# the end of the report and ask for one more generation to include the correct page count.


class PageCountBlocker(Flowable):
    def __init__(self):
        self.pageCount = 0
        self.width = 0
        self.height = 0
        self.firstRun = True

    def draw(self):
        self.pageCount = self.canv.getPageNumber()
        return

    def isSatisfied(self):
        global nbPages
        if self.firstRun:
            self.firstRun = False
            return False
        return True

    def isIndexing(self):
        return True

    def beforeBuild(self):
        return

    def afterBuild(self):
        return

    def notify(unused1, unused2, unused3):
        return

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'PageCountBlocker'
        str += 'pageCount: %s,\n' % self.pageCount
        str += 'width: %s,\n' % self.width
        str += 'firstRun: %s,\n' % self.firstRun
        str += ') noWord.#%s ' % 'PageCountBlocker'

        return str

# This class is a workaround to be able to draw vertical text. It will directly draw on
# the canvas, getting its content and style from the provided paragraph, so the width and
# height it will use is NOT dynamic, ensure you have enough space when you use it.


class VerticalText(Flowable):
    def __init__(self, paragraph, xoffset=0, yoffset=0):
        Flowable.__init__(self)
        self.paragraph = paragraph
        self.w = 0
        self.xoffset = xoffset
        self.yoffset = yoffset

    def wrap(self, w, h):
        w, h = self.paragraph.wrap(h, w)
        self.w = h
        self.h = optimalWidth(self.paragraph, 20*cm, 20*cm)
        return self.w, self.h

    def draw(self):
        self.paragraph.wrap(self.h, self.w)
        self.canv.saveState()
        self.canv.translate(self.xoffset + self.w, self.yoffset)
        self.canv.rotate(90)
        self.paragraph.drawOn(self.canv, 0, 0)
        self.canv.restoreState()

# Draw a text inside a colored circle, the hoffset can be used to fix the vertical
# alignment of the text inside the circle, as paragraph object seems so report wrong
# height when it uses custom fonts.


class Sticker(Flowable):
    def __init__(self, paragraph, backColor, padding=0.1*cm, hoffset=0):
        self.paragraph = paragraph
        self.backColor = backColor
        self.padding = padding
        self.hoffset = hoffset

    def wrap(self, availWidth, availHeight):
        maxWidth = min(availWidth, availHeight)
        w, h = self.paragraph.wrap(maxWidth, maxWidth)
        w = self.paragraph.minWidth()
        self.pw, self.ph = self.paragraph.wrap(w, h)
        self.radius = max(self.pw, self.ph) / 2 + self.padding
        return 2 * [2 * self.radius]

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.backColor)
        self.canv.circle(self.radius, self.radius,
                         self.radius, stroke=0, fill=1)
        self.paragraph.drawOn(
            self.canv, self.radius - self.pw / 2, self.radius - self.ph / 2 + self.hoffset)
        self.canv.restoreState()



# Draw a horizontal line
class Hline(Flowable):
    def __init__(self, width, color=colors.black, thickness=0.5, rounded=True, dashes=[1, 0], valign="MIDDLE"):
        self.width = width
        self.color = color
        self.thickness = thickness
        self.cap = 1 if rounded else 2
        self.dashes = dashes
        self.hpos = 0
        self.valign = valign

    def wrap(self, availWidth, availHeight):
        if self.valign == "TOP":
            self.hpos = 0
        if self.valign == "MIDDLE":
            self.hpos = availHeight/2
        if self.valign == "BOTTOM":
            self.hpos = availHeight
        return (self.width, self.thickness)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(self.thickness)
        self.canv.setStrokeColor(self.color)
        self.canv.setLineCap(self.cap)
        self.canv.setDash(*self.dashes)
        self.canv.line(-self.hpos, -self.hpos, self.width, -self.hpos)
        self.canv.restoreState()

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'Hline'
        str += 'width: %s,\n' % self.width
        str += 'color: %s,\n' % self.color
        str += 'thickness: %s,\n' % self.thickness
        str += 'cap: %s,\n' % self.cap
        str += 'dashes: %s,\n' % self.dashes
        str += 'valign: %s,\n' % self.valign
        str += ') noWord.#%s ' % 'Hline'

        return str



# Draw a progress bar
class ProgressBar(Flowable):
    def __init__(self, width, height, ratio, color=colors.blue, thickness=0.5):
        self.width  = width
        self.height = height
        self.ratio  = ratio
        self.color  = color
        self.thickness = thickness

    def wrap(self, *args):
        return (self.width, self.height)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(self.thickness)
        self.canv.setStrokeColor(self.color)
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height)
        self.canv.rect(0, 0, self.width*self.ratio, self.height, fill=1)
        self.canv.restoreState()

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'ProgressBar'
        str += 'width: %s,\n' % self.width
        str += 'height: %s,\n' % self.height
        str += 'ratio: %s,\n' % self.ratio
        str += 'color: %s,\n' % self.color
        str += 'thickness: %s,\n' % self.thickness
        str += ') noWord.#%s ' % 'Hline'

        return str


class Layout(Flowable):
    def __init__(self, template, builder, stickToPrevious=False):
        Flowable.__init__(self)
        self.template = template
        self.builder = builder
        self.stickToPrevious = stickToPrevious

    def changeLayout(self):
        self.builder.handle_nextPageTemplate(self.template)

    def draw(self):
        if not self.stickToPrevious: self.changeLayout()
