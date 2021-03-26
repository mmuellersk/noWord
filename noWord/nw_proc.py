#!/usr/bin/env python
import sys
import os
import datetime
import re

from timeit import default_timer as timer

import noWord.common.utils_fs as cmn_utils_fs

from noWord.common.NWGenerator import NWGenerator


def main():

    args = cmn_utils_fs.parserCommandLine()

    generator = NWGenerator(
        aSourcePath=args.source,
        aOutputPath=args.dest)

    nbPages = generator.process()


if __name__ == "__main__":
    main()
