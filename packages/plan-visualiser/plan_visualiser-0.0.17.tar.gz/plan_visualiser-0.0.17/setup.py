import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
VERSION = '0.0.17'

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'python-pptx',
      'dataclasses',
      'colour',
      'ddt==1.4.2',
      'openpyxl',
      ]
# et-xmlfile==1.1.0
# macholib==1.14
# measurement==3.2.0
# mpmath==1.2.1
# numpy==1.19.2
# openpyxl==3.0.7
# pandas==1.1.5
# pyinstaller==4.3
# pyinstaller-hooks-contrib==2021.1
# python-dateutil==2.8.1
# python-pptx==0.6.18
# pytz==2021.1
# six==1.16.0
# sympy==1.8
#
# behave>=1.2.5
# lxml>=3.1.0
# mock>=1.0.1
# Pillow>=3.3.2
# pyparsing>=2.0.1
# pytest>=2.5
# XlsxWriter>=0.5.7
# ]

setup(
      version=VERSION,
      install_requires=INSTALL_REQUIRES,
      )