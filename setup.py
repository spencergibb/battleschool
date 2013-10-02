#!/usr/bin/env python

import os
import sys
from glob import glob

sys.path.insert(0, os.path.abspath('lib'))
from battleschool import __version__, __author__
from distutils.core import setup

# find library modules
from battleschool.constants import DIST_MODULE_PATH

share_path = "./share/"
files = os.listdir(share_path)
data_files = []
for i in files:
    if os.path.isdir(os.path.join(share_path, i)):
        data_files.append((DIST_MODULE_PATH + i, glob(share_path + i + '/*')))

    #if os.path.isfile(os.path.join(share_path, i)):
    #    data_files.append((DIST_MODULE_PATH, share_path + i))

setup(name='battleschool',
      version=__version__,
      description='simple dev box provisioning',
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
