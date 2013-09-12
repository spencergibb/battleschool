#!/usr/bin/env python

import os
import sys
from glob import glob

sys.path.insert(0, os.path.abspath('lib'))
from battleschool import __version__, __author__
from distutils.core import setup

# find library modules
from battleschool.constants import DIST_MODULE_PATH
dirs = os.listdir("./library/")
data_files = []
for i in dirs:
    data_files.append((DIST_MODULE_PATH + i, glob('./library/' + i + '/*')))

setup(name='battleschool',
      version=__version__,
      description='Radically simple IT automation',
      author=__author__,
      author_email='spencer@32degre.es',
      url='http://32degre.es',
      license='GPLv3',
      install_requires=['ansible'],
      package_dir={'battleschool': 'lib/battleschool'},
      packages=[
          'battleschool',
          'battleschool.source',
      ],
      scripts=[
          'bin/battle',
          'bin/battle-bootstrap'
      ],
      data_files=data_files
)
