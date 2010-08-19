#!/usr/bin/python

from distutils.core import setup
from glob import glob

setup(name='python-creator',
      version='0.0.1',
      description='Clean python ide inspired by qt creator',
      long_description ="""Clean python ide inspired by qt creator
      """,
      author='Zhuo Wei',
      author_email='caymanww@gmail.com',
      license='New BSD License',
      url="http://code.google.com/p/python-creator",
      download_url="http://code.google.com/p/python-creator/downloads/list",
      platforms = ['Linux', 'Win32', 'MAC'],
      scripts=['pycreator'],
      packages = ['creator'],
      data_files = [
          ('share/python-creator/schemes/', glob('schemes/*')),
          ('share/applications/' ,['pycreator.desktop']),
      ],
      )
