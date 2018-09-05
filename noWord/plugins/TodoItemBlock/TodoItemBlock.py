#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER

from noWord.common.PluginInterface import PluginInterface


class TodoItemBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'todoitem'

    def init(self, context):
        # define used styles if not exists already
        if not 'lightgray' in context.styleSheet:
            context.styleSheet['lightgray'] = colors.HexColor("#bbbbbb")

        if not 'TODOIcon' in context.styleSheet:
            context.styleSheet['TODOIcon'] = ParagraphStyle(name="TODOIcon",
                                                            parent=context.styleSheet['default'],
                                                            fontName='FontAwesome',
                                                            alignment=TA_LEFT,
                                                            fontSize=10,
                                                            spaceBefore=8,
                                                            spaceAfter=8)

        if not 'TODOText' in context.styleSheet:
            context.styleSheet['TODOText'] = ParagraphStyle(name="TODOText",
                                                            parent=context.styleSheet['default'],
                                                            alignment=TA_LEFT,
                                                            fontSize=10,
                                                            spaceBefore=8,
                                                            spaceAfter=8)

        if not 'TODOTextDone' in context.styleSheet:
            context.styleSheet['TODOTextDone'] = ParagraphStyle(name="TODOTextDone",
                                                                parent=context.styleSheet['default'],
                                                                textColor=context.styleSheet["lightgray"],
                                                                alignment=TA_LEFT,
                                                                fontSize=10,
                                                                spaceBefore=8,
                                                                spaceAfter=8)

        if not 'TODOTextProgress' in context.styleSheet:
            context.styleSheet['TODOTextProgress'] = ParagraphStyle(name="TODOTextProgress",
                                                                    parent=context.styleSheet['default'],
                                                                    textColor=context.styleSheet["green"],
                                                                    alignment=TA_LEFT,
                                                                    fontSize=10,
                                                                    spaceBefore=8,
                                                                    spaceAfter=8)

    def prepare(self, block, context):
        pass

    def process(self, block, context):
        # title element
        title = block['title']

        # status element, defualt 'Open'
        status = self.getElemValue(block, 'status', 'Open')

        # width element
        width = block["width"] * \
            cm if "width" in block else context.doc.currentWidth()

        return self.makeTodoItem(context, title, status, width)

    def makeTodoItem(self, context, title, status, width):

        iconWidth = 0.5 * cm

        text = title
        icon = ''
        textStyle = context.styleSheet["default"]

        status = context.processTextCmds(status)

        if status == 'Open':
            text = title
            icon = '<font name="Symbols">&#xf096;</font>'
            textStyle = context.styleSheet["TODOText"]
        elif status == 'Done':
            text = '<strike>%s</strike>' % text
            icon = '<font name="Symbols">&#xf046;</font>'
            textStyle = context.styleSheet["TODOTextDone"]
        elif status == 'InProgress':
            text = '<b>%s</b>' % text
            icon = '<font name="Symbols">&#xf096;</font>'
            textStyle = context.styleSheet["TODOTextProgress"]
        else:
            text = 'Not defined'
            icon = ''
            textStyle = context.styleSheet["TODOText"]

        tableData = []

        tableData.append([context.paragraph(icon),
                          context.paragraph(text, textStyle)])

        todoTable = Table(tableData, [iconWidth, width - iconWidth])
        todoTable.hAlign = TA_LEFT
        todoTable.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                       ('VALIGN', (0, 0), (-1, -1), 'TOP')]))

        return [todoTable]
