
from reportlab.platypus import Flowable

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
