#!/usr/bin/env python

from hashlib import sha1

import common.utils_rp as cmn_utils_rp

# simulate link calculation
dummyLink = 1

# final link calculation
currentLink = 1


class TOCBuilder:
    def __init__(self):
        self.dummyCounter = {}
        self.chapterCounter = {}

    def getDummyChapterCounter(self, level):
        if not level in self.dummyCounter:
            self.dummyCounter[level] = 1

        return self.dummyCounter[level]

    def getCurrentChapterCounter(self, level):
        if not level in self.chapterCounter:
            self.chapterCounter[level] = 1

        return self.chapterCounter[level]

    def renderChapterCounter(self, level, sepChar='.'):
        chapters = ""

        for i in range(0, level):
            chapterCount = self.getCurrentChapterCounter(i) - 1
            chapters = chapters + str(chapterCount) + sepChar

        currentLevelCount = self.getCurrentChapterCounter(level)
        self.chapterCounter[level] = currentLevelCount + 1
        chapters = chapters + str(currentLevelCount)

        return chapters

    def renderDummyChapterCounter(self, level, sepChar='.'):
        chapters = ""

        for i in range(0, level):
            chapterCount = self.getDummyChapterCounter(i) - 1
            chapters = chapters + str(chapterCount) + sepChar

        currentLevelCount = self.getDummyChapterCounter(level)
        self.dummyCounter[level] = currentLevelCount + 1
        chapters = chapters + str(currentLevelCount)

        return chapters

    def preprocessTOCEntry(self, level):
        global dummyLink
        link = sha1(str(dummyLink).encode("utf-8")).hexdigest()
        dummyLink = dummyLink + 1
        return link

    def createTOCEntry(self, text, level):
        global currentLink
        link = sha1(str(currentLink).encode("utf-8")).hexdigest()
        tocEntry = cmn_utils_rp.TocEntry(level, text, link)
        currentLink = currentLink + 1
        return tocEntry
