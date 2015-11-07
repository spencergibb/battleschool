#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))
from battleschool import __version__, __author__
from distutils.core import setup

long_description = """
Development environment provisioning using ansible (http://docs.ansible.com),
ala boxen (http://boxen.github.com/) which uses puppet (http://puppetlabs.com/puppet/what-is-puppet) and
kitchenplan (https://github.com/kitchenplan/kitchenplan) which uses chef (http://docs.opscode.com/)
Built on and for macs, but should be usable on Linux
"""

package_dir = 'lib/battleschool'
package_data = []
top_dir = os.getcwd()
os.chdir(package_dir)
for dirpath, dirnames, filenames in os.walk('share'):
    data = [ os.path.join(dirpath, filename) for filename in filenames ]
    package_data.extend(data)
os.chdir(top_dir)

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
      package_dir={'battleschool': package_dir},
      package_data={'battleschool': package_data},
      packages=[
          'battleschool',
          'battleschool.source',
      ],
      scripts=[
          'bin/battle'
      ]
)
