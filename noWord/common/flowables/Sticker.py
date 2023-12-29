from reportlab.platypus import Flowable
from reportlab.lib.units import cm, mm


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


