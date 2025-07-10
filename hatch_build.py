#!/usr/bin/env python

import sys
import json
import os
import os.path

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from hatchling.metadata.plugin.interface import MetadataHookInterface


class JSONMetaDataHook(MetadataHookInterface):
    
    # Parse requirements.txt file in order to use it in setup.py
    def requirements(self, fname):
        with open(fname) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]



    def update(self, metadata):

        meta = {}
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(here, "noWord", "__init__.py"), encoding="utf-8") as f:
            exec(f.read(), meta)

        metadata["version"] = meta["__version__"]
        metadata["description"] = meta["__description__"]
        metadata["readme"] = {
            "file": "README.md",
            "content-type": "text/markdown"
        }
        metadata["requires-python"] = ">=3.9"
        metadata["license"] = meta["__license__"]
        metadata["license-files"] = ["LICEN[CS]E*"]
        metadata["authors"] = [
            {"name": meta["__author__"], "email": meta["__author_email__"]},
        ]
        metadata["classifiers"] = [
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
        metadata["urls"] = {
            "Homepage": "https://github.com/mmuellersk/noWord",
            "Issues": "https://github.com/mmuellersk/noWord/issues"
        }
        metadata["scripts"] = {
            "noWord": "noWord.nw_proc:main"
        }
        metadata["dependencies"] = self.requirements(os.path.join(
            os.path.dirname(__file__), 'requirements.txt'))

