#!/usr/bin/env python

from reportlab.platypus import Flowable
from reportlab.lib import colors
from reportlab.lib.units import cm, mm



# Draw a horizontal measurement arrow displaying available width
class Measure(Flowable):
    def __init__(self):
        self.height = 18
        self.color = colors.black
        self.thickness = 0.5
        
        self.fontsize = 12
        
        self.arrowHeight = 4
        self.arrowLength = 8
        
        pass
    
    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return (self.width, self.height)

    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(self.thickness)
        self.canv.setStrokeColor(self.color)
        # baseline
        self.canv.line( 0, self.arrowHeight, self.width, self.arrowHeight)
        
        # left arrow
        self.canv.line( 0, self.arrowHeight, self.arrowLength, 0)
        self.canv.line( 0, self.arrowHeight, self.arrowLength, self.arrowLength)
        
        # right arrow
        self.canv.line( self.width, self.arrowHeight, 
                       self.width-self.arrowLength, 0)
        self.canv.line( self.width, self.arrowHeight, 
                       self.width-self.arrowLength, self.arrowLength)
        
        label = '{width:.1f} cm'
        wd = label.format(width=(self.width/cm))
        
        self.canv.setFont("Roboto", self.fontsize)
        self.canv.drawString(0+self.width/2-20, self.arrowHeight+2, wd)
        
        self.canv.restoreState()

    def __str__(self):
        return self.__repr__(self)

    def __repr__(self):
        str = 'noWord.%s (\n' % 'Measure'
        str += 'width: %s,\n' % self.width
        str += ') noWord.#%s ' % 'Measure'

        return str
