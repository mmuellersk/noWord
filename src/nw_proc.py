#!/usr/bin/env python
import sys
import os
import datetime
import re

from timeit import default_timer as timer

import common.utils_fs as cmn_utils_fs

from common.NWGenerator import NWGenerator


def main():

    start = timer()

    args = cmn_utils_fs.parserCommandLine()

    generator = NWGenerator(
                aSourcePath=args.source,
                aOutputPath=args.dest)

    nbPages = generator.process()

    print ('noWord processing finished (%d page(s) rendered): %.5f seconds' %
        (nbPages, (timer() - start)))

if __name__ == "__main__": main()
