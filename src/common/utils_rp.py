
from reportlab.platypus import Flowable, BaseDocTemplate

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

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
