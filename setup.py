#!/usr/bin/env python

import sys, os, os.path, platform

from distutils.core import Command
from setuptools import setup, find_packages

import noWord as meta

if __name__ == '__main__':

  setup(
    name=meta.__name__,
    version=meta.__version__,
    description=meta.__description__,
    long_description=meta.__long_description__,
    author=meta.__author__,
    author_email=meta.__author_email__,
    license=meta.__license__,
    platforms=meta.__platforms__,
    url=meta.__uri__,
    install_requires=meta.__install_requires__,
    include_package_data=True,
    packages=[meta.__name__]
  )
