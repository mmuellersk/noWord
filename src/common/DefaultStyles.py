#!/usr/bin/env python

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER


styles = {}

# margins
styles["marginL"] = 78
styles["marginR"] = 78
styles["marginT"] = 106
styles["marginB"] = 78

# colors
styles['darkgray'] = colors.HexColor("#222222")

# Some characters usable as list bullets
longdash = u"\u2014"
bullet = "circle"
emptyBullet = u"\u25CB"
arrow = u"\u2192"

# Naming templates
styles["templates"] = {}
styles["templates"]["documentTitleTemplate"] = "{mainSubject}"
styles["templates"]["documentMetaTitleTemplate"] = "{shortDocumentType} {mainSubject} Rev. {revision}"
styles["templates"]["documentMetaAuthorTemplate"] = "noWord"
styles["templates"]["documentMetaSubjectTemplate"] = "{documentType}"
styles["templates"]["documentMetaKeywordsTemplate"] = "{shortDocumentType} {mainSubject}"
styles["templates"]["documentIdentifierTemplate"] = "{shortDocumentType}_{mainSubject}_{revision}.pdf"
styles["templates"]["outputFileTemplate"] = "{shortDocumentType}_{mainSubject}_{revision}.pdf"
styles["templates"]["revisionTemplate"] = "{shortDocumentType}_r.{revision}"

# list styles
styles["itemsInterSpace"] = 6
styles["listBullet"] = bullet
styles["listNumberFormat"] = "%s. "
styles["listBulletFontName"] = "Times-Roman"

# paragraph styles
styles['default'] = ParagraphStyle(name="BodyText",
                                   fontName='Times-Roman',
                                   fontSize=10,
                                   leading=12,
                                   leftIndent=0,
                                   rightIndent=0,
                                   firstLineIndent=0,
                                   alignment=TA_LEFT,
                                   spaceBefore=0,
                                   spaceAfter=0,
                                   bulletFontName='Times-Roman',
                                   bulletFontSize=10,
                                   bulletIndent=0,
                                   textColor=styles["darkgray"],
                                   backColor=None,
                                   wordWrap=None,
                                   borderWidth=0,
                                   borderPadding=0,
                                   borderColor=None,
                                   borderRadius=None,
                                   allowWidows=1,
                                   allowOrphans=0,
                                   textTransform=None,  # 'uppercase' | 'lowercase' | None
                                   endDots=None,
                                   splitLongWords=1)

styles['BodyText'] = ParagraphStyle(name="BodyText",
                                    parent=styles['default'],
                                    alignment=TA_JUSTIFY,
                                    fontSize=12,
                                    spaceBefore=6,
                                    spaceAfter=6)

styles['Heading1'] = ParagraphStyle(name="Heading1",
                                    parent=styles['default'],
                                    alignment=TA_LEFT,
                                    fontSize=20,
                                    spaceBefore=10,
                                    spaceAfter=10)

styles['Heading2'] = ParagraphStyle(name="Heading2",
                                    parent=styles['default'],
                                    alignment=TA_LEFT,
                                    fontSize=18,
                                    spaceBefore=9,
                                    spaceAfter=9)

styles['Heading3'] = ParagraphStyle(name="Heading3",
                                    parent=styles['default'],
                                    alignment=TA_LEFT,
                                    fontSize=16,
                                    spaceBefore=8,
                                    spaceAfter=8)

styles['ImageCaption'] = ParagraphStyle(name="ImageCaption",
                                    parent=styles['default'],
                                    alignment=TA_CENTER,
                                    fontSize=12,
                                    spaceBefore=4,
                                    spaceAfter=8)
