import os

from pip._internal.req import parse_requirements
from pip._internal.download import PipSession

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


__name__ = 'noWord'

__version__ = '1.0.0-alpha.1'

__description__ = 'non-WYSIWYG document generator'

__long_description__ = read(os.path.join(os.path.dirname(__file__), '../README.md'))

__author__ = 'Matthias Müller'

__author_email__ = 'mmueller.sk@gmail.com'

__license__ = 'GPL'

__platforms__ = 'Any'

__uri__ = 'https://github.com/mmuellersk/noWord'

__install_requires__ = requirements(os.path.join(os.path.dirname(__file__), '../requirements.txt'))
