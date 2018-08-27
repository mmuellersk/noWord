#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys



from noWord.common.NWGenerator import NWGenerator

import noWord.common.utils_fs as cmn_utils_fs


class NWTestCase:
    def __init__(self, testfolder, outputfolder):
        self.inputfolder = os.path.join(testfolder, 'input')
        self.reffile = os.path.join(testfolder, 'ref/ref.txt')
        self.outputfolder = outputfolder

        self.doc_info = cmn_utils_fs.loadYAML(
            os.path.join(self.inputfolder, 'doc_info.yaml'))

        self.context = {}

    def verifyDocInfo(self):
        if 'mainSubject' in self.doc_info:
            self.context['testname'] = self.doc_info['mainSubject']
        else:
            self.context['error'] = 'no mainSubject in doc_info'
            return False

        if 'description' in self.doc_info:
            self.context['testdesc'] = self.doc_info['description']
        else:
            self.context['error'] = 'no description in doc_info'
            return False

        return True

    def verifyGeneration(self):
        pdfFile = os.path.join(
            self.outputfolder, self.doc_info['mainSubject'] + '.pdf')


        if not os.path.exists(pdfFile):
            self.context['error'] = 'pdf file was not generated'
            return False

        self.pdfFile = pdfFile

        return True

    def compareResult(self):
        pass


    def outputResult(self):
        print(self.context)


    def run(self, result):
        if not self.verifyDocInfo():
            self.outputResult()
            return

        generator = NWGenerator(
            aSourcePath=self.inputfolder,
            aOutputPath=self.outputfolder,
            dumpContent=True)

        nbPages = generator.process()

        if not self.verifyGeneration():
            self.outputResult()
            return
