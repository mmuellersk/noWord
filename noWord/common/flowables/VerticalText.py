from reportlab.platypus import Flowable


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
    
    def optimalWidth(self, par, maxWidth, maxHeight):
        w, minHeight = par.wrap(maxWidth, maxHeight)
        totalMM = int(w / mm)

        while totalMM > 0:
            totalMM -= 1
            w, h = par.wrap(totalMM * mm, maxHeight)
            if h > minHeight:
                totalMM += 1
                break

        return totalMM * mm

    def wrap(self, w, h):
        w, h = self.paragraph.wrap(h, w)
        self.w = h
        self.h = self.optimalWidth(self.paragraph, 20*cm, 20*cm)
        return self.w, self.h

    def draw(self):
        self.paragraph.wrap(self.h, self.w)
        self.canv.saveState()
        self.canv.translate(self.xoffset + self.w, self.yoffset)
        self.canv.rotate(90)
        self.paragraph.drawOn(self.canv, 0, 0)
        self.canv.restoreState()
