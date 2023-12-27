#!/usr/bin/env python

from reportlab.platypus import Flowable
from reportlab.lib import utils, colors



# Draw a horizontal line
class HLine(Flowable):
    def __init__(self, width, color=colors.black, thickness=0.5, rounded=True, dashes=[1, 0]):
        self.width = width
        self.color = color
        self.thickness = thickness
        self.cap = 1 if rounded else 2
        self.dashes = dashes

    def wrap(self, availWidth, availHeight):
        return (self.width, self.thickness)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(self.thickness)
        self.canv.setStrokeColor(self.color)
        self.canv.setLineCap(self.cap)
        self.canv.setDash(*self.dashes)
        self.canv.line( 0, 0, self.width, 0)
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
