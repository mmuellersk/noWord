#!/usr/bin/env python

import sys
import os
import os.path
import platform

from pip._internal.req import parse_requirements
from pip._internal.download import PipSession

from distutils.core import Command
from setuptools import setup, find_packages

import noWord as meta


# Parse requirements.txt file in order to use it in setup.py
def requirements(fname):
    install_reqs = parse_requirements(fname, session=PipSession())
    return [str(ir.req) for ir in install_reqs]

# Read long description from README.md


def read(fname):
    inf = open(os.path.join(os.path.dirname(__file__), fname))
    out = "\n" + inf.read().replace("\r\n", "\n")
    inf.close()
    return out


if __name__ == '__main__':

    setup(
        name=meta.__name__,
        version=meta.__version__,
        description=meta.__description__,
        long_description=read(os.path.join(
            os.path.dirname(__file__), 'README.md')),
        author=meta.__author__,
        author_email=meta.__author_email__,
        license=meta.__license__,
        platforms=meta.__platforms__,
        url=meta.__uri__,
        install_requires=requirements(os.path.join(
            os.path.dirname(__file__), 'requirements.txt')),
        include_package_data=True,
        packages=[meta.__name__],
        entry_points={
            "console_scripts": ['noWord = noWord.nw_proc:main']
        }
    )
