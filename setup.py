#!/usr/bin/env python

import os
import sys
from glob import glob

sys.path.insert(0, os.path.abspath('lib'))
from battleschool import __version__, __author__
from distutils.core import setup

# find library modules
from battleschool.constants import DIST_MODULE_PATH

long_description = """
Development environment provisioning using ansible (http://docs.ansible.com),
ala boxen (http://boxen.github.com/) which uses puppet (http://puppetlabs.com/puppet/what-is-puppet) and
kitchenplan (https://github.com/kitchenplan/kitchenplan) which uses chef (http://docs.opscode.com/)
Built on and for macs, but should be usable on Linux
"""

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
      long_description=long_description,
      author=__author__,
      author_email='spencer@gibb.us',
      url='http://spencer.gibb.us',
      download_url='https://github.com/spencergibb/battleschool/releases',
      license='Apache License, Version 2.0',
      # added jinja2 and pyyaml to fix installs under homebrew pip
      install_requires=[
          'ansible >= 1.9.1',
          'jinja2',
          'pyyaml'
      ],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Environment :: MacOS X",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 2.7",
          "Topic :: System :: Installation/Setup"
      ],
      keywords="provisioning setup install",
      package_dir={'battleschool': 'lib/battleschool'},
      packages=[
          'battleschool',
          'battleschool.source',
      ],
      scripts=[
          'bin/battle'
      ],
      data_files=data_files
)
