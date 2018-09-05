#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import html

# This class provides a framework for the execution of one unit test.


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
        self.context['passed'] = False

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
        outputFile = os.path.join(
            self.outputfolder, self.doc_info['mainSubject'] + '.pdf.txt')

        if not os.path.exists(outputFile):
            self.context['error'] = 'output file was not generated'
            return False

        self.context['outputFile'] = outputFile

        outputPdfFile = self.doc_info['mainSubject'] + '.pdf'

        if not os.path.exists(os.path.join(self.outputfolder, self.doc_info['mainSubject'] + '.pdf')):
            self.context['error'] = 'pdf file was not generated'
            return False

        self.context['outputPdfFile'] = outputPdfFile

        return True

    # Text file comparioson based on:
    # https://www.opentechguides.com/how-to/article/python/58/python-file-comparison.html
    def compareResult(self):
        # Open file for reading in text mode (default mode)
        f1 = open(self.context['outputFile'])
        f2 = open(self.reffile)

        # Read the first line from the files
        f1_line = f1.readline()
        f2_line = f2.readline()

        # Initialize counter for line number
        line_no = 1

        error = ''
        passed = True

        # Loop if either file1 or file2 has not reached EOF
        while f1_line != '' or f2_line != '':

            # Strip the leading whitespaces
            f1_line = f1_line.rstrip()
            f2_line = f2_line.rstrip()

            # Compare the lines from both file
            if f1_line != f2_line:

                prefix = "Line-%d" % line_no

                # If a line does not exist on file2 then mark the output with + sign
                if f2_line == '' and f1_line != '':
                    passed = False
                    error += html.escape(">+ " + prefix + f1_line) + '<br/>'
                # otherwise output the line on file1 and mark it with > sign
                elif f1_line != '':
                    passed = False
                    error += html.escape("<  " + prefix + f1_line) + '<br/>'
                # If a line does not exist on file1 then mark the output with + sign
                if f1_line == '' and f2_line != '':
                    passed = False
                    error += html.escape("<+ " + prefix + f2_line) + '<br/>'
                # otherwise output the line on file2 and mark it with < sign
                elif f2_line != '':
                    passed = False
                    error += html.escape("<  " + prefix + f2_line) + '<br/>'

            # Read the next line from the file
            f1_line = f1.readline()
            f2_line = f2.readline()

            # Increment line counter
            line_no += 1

        # Close the files
        f1.close()
        f2.close()

        self.context['error'] = error
        self.context['passed'] = passed

        return self.context['passed']

    def finaliseTest(self):
        if not self.context['passed']:
            print("Test FAILED: " + self.context['testname'])

            self.context['passedStr'] = 'FAILED'
            self.context['passedStyle'] = 'RedText'
        else:
            print("Test passed: " + self.context['testname'])
            self.context['passedStr'] = 'PASSED'
            self.context['passedStyle'] = 'GreenText'

        if self.context['error'] == '':
            self.context['error'] = 'Non'

    def run(self):
        if not self.verifyDocInfo():
            return

        generator = NWGenerator(
            aSourcePath=self.inputfolder,
            aOutputPath=self.outputfolder,
            dumpContent=True)

        nbPages = generator.process()

        if not self.verifyGeneration():
            return

        self.compareResult()

        self.finaliseTest()
