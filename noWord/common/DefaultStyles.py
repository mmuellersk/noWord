#!/usr/bin/env python
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER


assetsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
arimoDir = os.path.join(assetsDir, "Arimo")

# Choosing font
pdfmetrics.registerFont(
    TTFont('Symbols', os.path.join(assetsDir, "FontAwesome.ttf")))

pdfmetrics.registerFont(
    TTFont('Arimo', os.path.join(arimoDir, "Arimo-Regular.ttf")))
pdfmetrics.registerFont(
    TTFont('ArimoBold', os.path.join(arimoDir, "Arimo-Bold.ttf")))
pdfmetrics.registerFont(
    TTFont('ArimoItalic', os.path.join(arimoDir, "Arimo-Italic.ttf")))
pdfmetrics.registerFont(
    TTFont('ArimoBoldItalic', os.path.join(arimoDir, "Arimo-BoldItalic.ttf")))

pdfmetrics.registerFontFamily("Arimo", normal="Arimo",
                              bold="ArimoBold", italic="ArimoItalic", boldItalic="ArimoBoldItalic")
styles = {}

# margins
styles["marginL"] = 78
styles["marginR"] = 78
styles["marginT"] = 106
styles["marginB"] = 78
styles["headerMargin"] = 0.2 * cm
styles["footerMargin"] = 1.2 * cm

# colors
styles['darkgray'] = colors.HexColor("#222222")
styles['green'] = colors.HexColor("#00aa00")
styles['darkyellow'] = colors.HexColor("#999900")
styles['darkblue'] = colors.HexColor("#0077b3")
styles['lightblue'] = colors.HexColor("#cceeff")
styles['red'] = colors.HexColor("#AA0000")
styles['green'] = colors.HexColor("#00AA00")

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
styles["itemsInterSpace"] = 0
styles["listBullet"] = bullet
styles["listNumberFormat"] = "%s. "
styles["listBulletFontName"] = "Times-Roman"
styles["listBulletFontSize"] = 10

# table styles
styles["headerBackground"] = colors.lightgrey
styles["highlightBackground"] = colors.HexColor("#ffff00")

# paragraph styles
styles['default'] = ParagraphStyle(name="default",
                                   fontName='Arimo',
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
                                    fontSize=10,
                                    spaceBefore=6,
                                    spaceAfter=6)


styles["HeaderRight"] = ParagraphStyle(name="HeaderRight",
                                       parent=styles['default'],
                                       fontSize=8,
                                       alignment=TA_RIGHT)


styles["FooterRight"] = ParagraphStyle(name="FooterRight",
                                       parent=styles['default'],
                                       fontSize=8,
                                       alignment=TA_RIGHT)

styles['GreenText'] = ParagraphStyle(name="GreenText",
                                     parent=styles['default'],
                                     textColor=styles["green"])

styles['RedText'] = ParagraphStyle(name="RedText",
                                   parent=styles['default'],
                                   textColor=styles["red"])

styles['Code'] = ParagraphStyle(name="Code",
                                parent=styles['default'],
                                fontName='Courier',
                                fontSize=10,
                                textColor=colors.white,
                                backColor=colors.black,
                                spaceBefore=6,
                                spaceAfter=6,
                                borderPadding=3)
