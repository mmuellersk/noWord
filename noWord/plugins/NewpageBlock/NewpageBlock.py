#!/usr/bin/env python

import sys
sys.path.insert(0, '..')

from reportlab.platypus import PageBreak, CondPageBreak, PageTemplate, Frame
import reportlab.lib.pagesizes as pagesizes

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_rp as cmn_utils_rp
from reportlab.lib.units import cm, mm


class NewpageBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'newpage'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        if "layout" in block:
            pagedef = block["layout"]
            if isinstance(pagedef, str):
                for t in context.doc.doc.pageTemplates:
                    if t.id == pagedef:
                        template = t
                        break
            else:
                style = context.doc.style
                identifier = pagedef["name"] if "name" in pagedef else str(len(context.doc.doc.pageTemplates))

                # Get page size, can be an existing reportlab definition (A5, A4, A3, ...) or a custom size
                pageSize = pagedef["size"]
                if isinstance(pageSize, str) and hasattr(pagesizes, pageSize):
                    size = getattr(pagesizes, pageSize)
                else:
                    size = (pageSize[0]*cm, pageSize[1]*cm)

                # Compute page orientation if needed (supported keys are landscape and portrait)
                if "orientation" in pagedef and pagedef["orientation"] in ["portrait", "landscape"]:
                    size = getattr(pagesizes, pagedef["orientation"])(size)

                template = PageTemplate(id=identifier,
                                        frames=Frame(style["marginL"],
                                        style["marginB"],
                                        size[0] - style["marginL"] - style["marginR"],
                                        size[1] - style["marginT"] - style["marginB"]),
                                        onPageEnd=context.doc.drawDecoration,
                                        pagesize=size)
                context.doc.doc.addPageTemplates(template)

            context.doc.pageRect = template.pagesize

            # Force the page layout to change just after the previous flowable has been drawn
            stick = "onPrevious" in block and block["onPrevious"]
            blocks = [cmn_utils_rp.Layout(template.id, context.doc.doc, stick)]
            if not stick: blocks.append(PageBreak())
            return blocks
        else:
            return [CondPageBreak(0.9 * context.doc.currentHeight())]
