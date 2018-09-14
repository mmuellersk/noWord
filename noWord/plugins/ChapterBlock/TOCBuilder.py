#!/usr/bin/env python

from hashlib import sha1

import noWord.common.utils_rp as cmn_utils_rp

import noWord.common as cmn

class TOCBuilder:
    def __init__(self):
        self.chapterCounter = {}
        self.lastLevel = 0
        cmn.initialize()

    def getCurrentChapterCounter(self, level):
        if not level in self.chapterCounter:
            self.chapterCounter[level] = 1

        return self.chapterCounter[level]

    def resetTocCounter(self, level, value=1):
        for lev in [lev for lev in self.chapterCounter if lev >= level]:
            self.chapterCounter[lev] = value

    def renderChapterCounter(self, level, sepChar='.'):
        chapters = ""

        for i in range(0, level):
            chapterCount = self.getCurrentChapterCounter(i) - 1
            chapters = chapters + str(chapterCount) + sepChar

        currentLevelCount = self.getCurrentChapterCounter(level)
        self.chapterCounter[level] = currentLevelCount + 1
        chapters = chapters + str(currentLevelCount)

        if level < self.lastLevel:
            self.resetTocCounter(level + 1)
        self.lastLevel = level

        return chapters

    def createTOCEntry(self, text, level):
        cmn.currentLink += 1
        link = sha1(str(cmn.currentLink).encode("utf-8")).hexdigest()
        tocEntry = cmn_utils_rp.TocEntry(level, text, link)
        return tocEntry
