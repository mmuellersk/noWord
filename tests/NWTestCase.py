#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from timeit import default_timer as timer

sys.path.insert(0, '.')

from noWord.common.NWGenerator import NWGenerator


class NWTestCase:
    def __init__(self, inputfolder, outputfolder):
        self.inputfolder = os.path.join(inputfolder,'input')
        self.reffolder = os.path.join(inputfolder,'ref')
        self.outputfolder = outputfolder

    def run(self):
        start = timer()

        generator = NWGenerator(
            aSourcePath=self.inputfolder,
            aOutputPath=self.outputfolder)

        nbPages = generator.process()

        duration = (timer() - start)
