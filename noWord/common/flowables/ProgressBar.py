#!/usr/bin/env python

from reportlab.platypus import Flowable
from reportlab.lib import colors


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
