#!/usr/bin/env python
from reportlab.platypus import Paragraph, Table, TableStyle, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib import colors


def drawGraphicSignature(canvas, doc, data, style):
    # The graphic signature is sized proportionally to the page height
    decoBottom = 0.9 * canvas._pagesize[1]
    decoTop = 0.5 * canvas._pagesize[1]
    width = 0.006 * canvas._pagesize[1]

    canvas.saveState()
    p = canvas.beginPath()
    p.rect(0, decoBottom, width, decoTop - decoBottom)
    canvas.clipPath(p, stroke=0)
    canvas.linearGradient(0, decoBottom, 0, decoTop,
                          (style["darkgray"], style["darkblue"]), extend=False)
    canvas.setStrokeColor(style["darkgray"])
    canvas.setFillColor(style["darkgray"])
    canvas.rect(0, decoBottom, width, decoBottom - decoTop, fill=1)
    canvas.restoreState()


def drawHeader(canvas, doc, data, style):
    docWidth = doc.pageTemplate.pagesize[0] - doc.leftMargin - doc.rightMargin
    docHeight = doc.pageTemplate.pagesize[1] - doc.topMargin - doc.bottomMargin

    # Header
    content = data["documentIdentifierTemplate"] + "<br/>"
    content += ("Revision " + str(data["revision"])
                ) if "revision" in data else "<br/>"
    header = Paragraph(content, style["HeaderRight"])
    w, h = header.wrap(docWidth, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, docHeight +
                  doc.topMargin + h - style["headerMargin"])


def drawFooter(canvas, doc, data, style):

    # Page number and total
    drawPageNums(canvas, doc, data, style)


def drawPageNums(canvas, doc, data, style):
    docWidth = doc.pageTemplate.pagesize[0] - doc.leftMargin - doc.rightMargin
    pagenums = Paragraph("Page " + str(canvas.getPageNumber()) +
                         " of " + str(data["pageCount"]), style["FooterRight"])
    w, h = pagenums.wrap(docWidth, doc.bottomMargin)
    pagenums.drawOn(canvas, doc.leftMargin, style["footerMargin"])
