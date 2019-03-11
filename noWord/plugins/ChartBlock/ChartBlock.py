#!/usr/bin/env python
import os
import sys
sys.path.insert(0, '...')


from reportlab.platypus import Paragraph, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from noWord.common.PluginInterface import PluginInterface
import noWord.common.utils_rp as cmn_utils_rp


class ChartBlock(PluginInterface):
    def __init__(self):
        self.padding = 0.4 * cm
        pass

    def Name(self):
        return 'chart'

    def init(self, context):
        pass

    def prepare(self, block, context):
        pass

    def process(self, block, context):

        # width and height element
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()
        height = block["height"] * \
            cm if "height" in block else 5 * cm

        mode = self.getElemValue(block, 'mode', 'linechart')

        data = block["data"] if "data" in block else None
        if isinstance(data, str):
            data = context.getResource(
                context.resources, block["data"])

        plotdata = block["plotdata"] if "plotdata" in block else None
        if isinstance(plotdata, str):
            plotdata = context.getResource(
                context.resources, block["plotdata"])

        xvalues = block["xvalues"] if "xvalues" in block else None
        if isinstance(xvalues, str):
            xvalues = context.getResource(
                context.resources, block["xvalues"])

        linecolors = self.getElemValue(block, 'linecolors', [])

        if mode == 'linechart':
            return self.makeLineChart(context, width, height, data)
        if mode == 'barchart':
            return self.makeBarChart(context, width, height, data)
        if mode == 'plotchart':
            return self.makePlotChart(context, width, height, plotdata, xvalues, linecolors)
        else:
            return []

    def makeLineChart(self, context, width, height, data):
        content = []

        drawing = Drawing(width, height)

        lp = HorizontalLineChart()
        lp.x = 0
        lp.y = 0
        lp.height = height
        lp.width = width
        lp.data = data
        lp.joinedLines = 1

        drawing.add(lp)

        content.append( drawing )

        return content

    def makeBarChart(self, context, width, height, data):
        content = []

        drawing = Drawing(width, height)

        lp = VerticalBarChart()
        lp.x = 0
        lp.y = 0
        lp.height = height
        lp.width = width
        lp.data = data

        drawing.add(lp)

        content.append( drawing )

        return content

    def makePlotChart(self, context, width, height, data, xvalues, linecolors):
        content = []

        drawing = Drawing(width, height)

        plot = LinePlot()
        plot.x = 0
        plot.y = self.padding
        plot.height = height - 2 * self.padding
        plot.width = width
        plot.data = data
        plot.joinedLines = 1
        plot.lineLabelFormat = '%2.0f'

        i = 0
        for color in linecolors :
            plot.lines[i].strokeColor = colors.HexColor(color)
            i = i+1

        plot.lines[0].name = 'test'

        if xvalues :
            plot.xValueAxis.valueSteps = xvalues

        drawing.add(plot)

        content.append( drawing )

        return content
