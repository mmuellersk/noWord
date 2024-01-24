from reportlab.platypus import Flowable
from reportlab.lib import utils, colors
from reportlab.lib.units import cm, mm

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl


class PDFImage(Flowable):
    def __init__(self, filename, width):
        pages = PdfReader(filename).pages

        # use first page only of pdf document
        self.page = pagexobj(pages[0])

        self.width = width
        self.height = width / (self.page.BBox[2] / self.page.BBox[3])
        
        print(self.page.BBox)

    def wrap(self, availWidth, availHeight):
        return (self.width, self.height)

    def draw(self):
        factor = 1 / (self.page.BBox[2] / self.width)

        # Use the canvas in absolute coordinates
        self.canv.saveState()
        self.canv.scale(factor, factor)
        self.canv.doForm(makerl(self.canv, self.page))
        self.canv.restoreState()

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'PDFImage'
        str += 'width: %s,\n' % self.width
        str += 'height: %s,\n' % self.height
        str += ') noWord.#%s ' % 'PDFImage'

        return str