import os
import re
import mimetypes as mime

from reportlab.platypus import Flowable, BaseDocTemplate, Image, Spacer
from reportlab.platypus import ListFlowable, Table, TableStyle
from reportlab.lib import utils, colors

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl


allowedImages = [
    "image/jpeg",
    "image/png",
    "image/x-ms-bmp",
    "image/tiff",
    "image/gif"]


def makeList(context, items, numbered=False, start=1, itemSpace=6):
    if not hasattr(context, 'lastListCounter'):
        context.lastListCounter = 1

    if type(start) is str and start == "continue":
        start = context.lastListCounter

    elif type(start) is not int:
        start = 1

    kwargs = {"bulletDedent": 15,
              "leftIndent": 30,
              "spaceAfter": 0,
              "bulletFontName": context.styleSheet["listBulletFontName"],
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
                repeatRows=0, border=0.5):
    # It is possible to render a table without headers
    nbCols = max(len(headers), len(lines[0]))
    nbLines = len(lines) + 1 if len(headers) > 0 else 0

    tableData = []
    headersLine = []
    style = [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
             ('VALIGN', (0, 0), (-1, -1), 'TOP')]
    if border > 0:
        style.append(('GRID', (0, 0), (-1, -1), border, colors.black))

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

    for line in lines:
        lineData = []
        for col in line:
            if isinstance(col, str):
                lineData.append(
                    context.paragraph(col, context.styleSheet["BodyText"]))
            elif isinstance(col, list):
                context.processFuncObj(col, context, path)
                lineData.append(context.process())

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
        pages = PDFPage(filename, width=width, index=0)
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

# Wrap a PDF page (xobject) as a reportlab flowable


class PDFPage(Flowable):
    def __init__(self, filename, width, index):
        pages = PdfReader(filename).pages
        self.page = pagexobj(pages[index])
        self.width = width
        self.height = width / (self.page.BBox[2] / self.page.BBox[3])

    def wrap(self, *args):
        return (self.width, self.height)

    def draw(self):
        factor = 1 / (self.page.BBox[2] / self.width)

        self.canv.saveState()
        self.canv.scale(factor, factor)
        self.canv.doForm(makerl(self.canv, self.page))
        self.canv.restoreState()

# This empty flowable is provides a trigger that will call a function when it is rendered.


class TriggerFlowable(Flowable):
    def __init__(self, callback):
        Flowable.__init__(self)
        self.callback = callback

    def callback(self):
        return

    def draw(self):
        self.callback()

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

# Doc Template with table of contents


class DocTemplateWithToc(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == 'TocEntry':
            level = flowable._level
            text = flowable._text
            link = flowable._link
            self.notify('TOCEntry', (level, text, self.page, link))
            self.canv.bookmarkPage(link)
            self.canv.addOutlineEntry(re.sub("<[^>]*>", "", text), link, level)

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

# Draw a horizontal line


class Hline(Flowable):
    def __init__(self, width, color=colors.black, thickness=0.5, rounded=True, dashes=[1, 0]):
        self.width = width
        self.color = color
        self.thickness = thickness
        self.cap = 1 if rounded else 2
        self.dashes = dashes

    def wrap(self, *args):
        return (self.width, self.thickness)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(self.thickness)
        self.canv.setStrokeColor(self.color)
        self.canv.setLineCap(self.cap)
        self.canv.setDash(*self.dashes)
        self.canv.line(0, 0, self.width, 0)
        self.canv.restoreState()
