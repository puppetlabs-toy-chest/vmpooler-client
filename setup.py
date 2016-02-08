#!/usr/bin/env python

#===================================================================================================
# Imports
#===================================================================================================
try:
  # setuptools is used to build wheels. Fallback to distutils if it isn't available.
  from setuptools import setup
except ImportError:
  from distutils.core import setup

from os import path
from vmpooler_client.version import version


def load_readme(readme_filename):
    return open(path.join(path.dirname(__file__), readme_filename)).read()


#===================================================================================================
# Globals
#===================================================================================================
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Utilities',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7']

#===================================================================================================
# Main
#===================================================================================================
setup(name='vmpooler-client',
      version=version,
      description='Manage resources in the vmpooler service from the command-line.',
      long_description=load_readme("README.rst"),
      author='Ryan Gard',
      author_email='ryan.gard@puppetlabs.com',
      url='https://github.com/puppetlabs/vmpooler-client',
      packages=['vmpooler_client', 'vmpooler_client.commands'],
      scripts=['vmpooler_client_app.py'],
      classifiers=CLASSIFIERS)
