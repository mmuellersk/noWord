import os
import re
import mimetypes as mime
from hashlib import sha1
import sys

from reportlab.platypus import Paragraph, Flowable, BaseDocTemplate
from reportlab.platypus import KeepTogether, Image, Spacer
from reportlab.platypus import CondPageBreak
from reportlab.platypus import Preformatted
from reportlab.platypus import ListFlowable, Table, TableStyle
from reportlab.lib import utils, colors
from reportlab.lib.units import cm, mm

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

import noWord.common as cmn
from noWord.common.flowables.PDFImage import PDFImage

from PIL import Image as PILImage, ExifTags


allowedImages = [
    "image/jpeg",
    "image/png",
    "image/x-ms-bmp",
    "image/tiff",
    "image/gif"]

def resolveAllTokens(context, text, style=None):
    if style is None:
        style = context.styleSheet["BodyText"]
    p = Paragraph(context.processTextCmds(text), style)
    context.doc.paragraphs.append(p)
    return p

def resolveAllTokensForPre(context, text):
    style = context.styleSheet["Pre"]
    p = Preformatted(context.processTextCmds(text), style)
    return p


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
            resolveAllTokens(context, "<b>" + col + "</b>", context.styleSheet["BodyText"]))
    if len(headers) > 0:
        tableData.append(headersLine)
        style.append(("BACKGROUND", (0, 0), (-1, 0),
                      context.styleSheet["headerBackground"]))

    for lineNumber in highlights:
        lineNumber = lineNumber + 1 if len(headersLine) > 0 else 0
        style.append(("BACKGROUND", (0, lineNumber), (-1, lineNumber),
                      context.styleSheet["highlightBackground"]))

    for item in bgcolor:
        color = item["color"]
        if color in context.styleSheet :
            color = context.styleSheet[color]
        else:
            color = context.processTextCmds(color)


        style.append(("BACKGROUND",
                      (item["from"][0], item["from"][1]),
                      (item["to"][0], item["to"][1]),
                     color))

    if len(customStyle) > 0:
        style = context.styleSheet[customStyle]

    for line in lines:
        lineData = []
        for col in line:
            if isinstance(col, list):
                content = []
                content.extend(context.processFuncObj(col, context, path))
                lineData.append(content)
            else:
                lineData.append(
                    resolveAllTokens( context, col, context.styleSheet["BodyText"]))

        tableData.append(lineData)

    table = Table(tableData, widths, heights, repeatRows=repeatRows)
    table.setStyle(TableStyle(style))
    table.hAlign = halign

    content = []
    content.append(table)
    return content

def makeChapter(context, text, level, toc, numbered, sepChar, style, label=None):
    content = []

    finalText = context.processTextCmds(text)

    numberLabel = ''

    if numbered:
        numberLabel = context.toc.renderChapterCounter(level, sepChar)
        finalText = numberLabel + sepChar + ' ' + finalText

    tocEntry = context.toc.createTOCEntry(finalText, level)

    chapter = resolveAllTokens( context, "<a name=\"%s\"/>%s" %
                                (tocEntry._link, finalText), style)
    context.doc.paragraphs.append(tocEntry)
    context.doc.paragraphs.append(chapter)

    result = [CondPageBreak(2 * cm)]
    if toc:
        result.append(tocEntry)

    result.append(chapter)
    result.append(Spacer(1, 12 if level == 0 else 6))
    content.append(KeepTogether(result))

    if label and numbered:
        anchor = {}
        anchor['_name'] = tocEntry._link
        anchor['_label'] = numberLabel
        anchor['_text'] = text
        if anchor['_name'] in context.anchors:
            print("Warning: overwriting bookmark " + anchor['_name'])
        context.anchors[label] = anchor

    return content


def orient_image(path, inplace=False):
    with PILImage.open(path) as img:
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = img._getexif()
            if exif and orientation in exif:
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # No EXIF data or Orientation tag
            pass

        # Save to the original image or a new one
        if not inplace:
            path = path.replace('.jpg', '_oriented.jpg')

        img.save(path)
        return path


def getImage(filename, width, dummy=False):
    filename = os.path.normpath(filename)

    filename = orient_image(filename, inplace=True)

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
        img = PDFImage(filename, width)
        height = img.height

    else:
        print("Unsupported image type " + imageType + " for " + filename)
        img = Spacer(width, width / 2)
        height = img.width / 2

    return DummyFlowable(Spacer(width, height), img, dummy)


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
