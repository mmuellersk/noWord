#!/usr/bin/env python

from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.platypus import Flowable, Table, TableStyle, Spacer, Frame
from reportlab.lib import utils
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4



MARGIN_SIZE = 20 * mm
PAGE_SIZE = A4


class NWDocument :
    def __init__(self, aFileName) :
        self.doc = BaseDocTemplate(filename = aFileName,
            outputfilepagesize = PAGE_SIZE,
            leftMargin = MARGIN_SIZE, rightMargin = MARGIN_SIZE,
            topMargin = MARGIN_SIZE, bottomMargin = MARGIN_SIZE)
        main_frame = Frame(MARGIN_SIZE, MARGIN_SIZE,
            PAGE_SIZE[0] - 2 * MARGIN_SIZE, PAGE_SIZE[1] - 2 * MARGIN_SIZE,
            leftPadding = 0, rightPadding = 0, bottomPadding = 0,
            topPadding = 0, id = 'main_frame')

        main_template = PageTemplate(id = 'main_template',
            frames = [main_frame])
        self.doc.addPageTemplates([main_template])

    def build(self,content) :
        self.doc.build(content)
