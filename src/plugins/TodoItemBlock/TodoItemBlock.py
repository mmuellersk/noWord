#!/usr/bin/env python

import sys
sys.path.insert(0, '...')

from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.units import cm

from common.PluginInterface import PluginInterface


class TodoItemBlock(PluginInterface):
    def __init__(self):
        pass

    def Name(self):
        return 'todoitem'

    def init(self, context):
        pass

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

        iconWidth = 0.4 * cm

        text = title
        icon = ''
        textStyle = context.styleSheet["default"]

        status = context.processTextCmds(status)

        if status == 'Open':
            text = title
            icon = '&#xf096;'
            textStyle = context.styleSheet["TODOText"]
        elif status == 'Done':
            text = '<strike>%s</strike>' % text
            icon = '&#xf046;'
            textStyle = context.styleSheet["TODOTextDone"]
        elif status == 'InProgress':
            text = '<b>%s</b>' % text
            icon = '&#xf096;'
            textStyle = context.styleSheet["TODOTextProgress"]
        else:
            text = 'Not defined'
            icon = ''
            textStyle = context.styleSheet["TODOText"]

        tableData = []

        tableData.append([context.paragraph(icon, context.styleSheet["TODOIcon"]),
                          context.paragraph(text, textStyle)])

        todoTable = Table(tableData, [iconWidth, width - iconWidth])

        todoTable.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                       ('VALIGN', (0, 0), (-1, -1), 'TOP')]))

        return [todoTable]
