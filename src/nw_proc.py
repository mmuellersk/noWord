#!/usr/bin/env python
import sys
import os
import datetime
import re

from timeit import default_timer as timer

import common.utils_fs as cmn_utils_fs

from common.generator import NWGenerator


def main():

    start = timer()

    args = cmn_utils_fs.parserCommandLine()

    # Load general prefs
    docInfos = cmn_utils_fs.deserialize(
        os.path.join(args.source,
        "doc_info.yaml"))

    generator = NWGenerator(
                docInfos,
                aSourcePath=args.source,
                aOutputPath=args.dest)

    generator.process()

    print ('noWord processing finished: %.5f seconds' % (timer() - start))

if __name__ == "__main__": main()
