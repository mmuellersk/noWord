#!/usr/bin/env python

from hashlib import sha1

import common.utils_rp as cmn_utils_rp

currentLink = 1


class TOCBuilder:
    def __init__(self):
        self.chapterCounter = {}

    def getCurrentChapterCounter(self, level):
        if not level in self.chapterCounter:
            self.chapterCounter[level] = 1

        return self.chapterCounter[level]

    def incrementChapterCounter(self, level):
        currentLevelCount = self.getCurrentChapterCounter(level)
        self.chapterCounter[level] = currentLevelCount + 1

    def renderChapterCounter(self, level, sepChar='.'):
        chapters = ""

        for i in range(0, level):
            chapterCount = self.getCurrentChapterCounter(i) - 1
            chapters = chapters + str(chapterCount) + sepChar

        currentLevelCount = self.getCurrentChapterCounter(level)
        self.chapterCounter[level] = currentLevelCount + 1
        chapters = chapters + str(currentLevelCount)

        return chapters

    def createTOCEntry(self, text, level):
        global currentLink
        link = sha1(str(currentLink).encode("utf-8")).hexdigest()
        tocEntry = cmn_utils_rp.TocEntry(level, text, link)
        currentLink = currentLink + 1
        return tocEntry
