'''
Setup Script for PyCache
This will install the pycache library into your system
'''


import os
from setuptools import setup
from setuptools import find_packages


__status__      = "Package"
__copyright__   = "Copyright 2021"
__license__     = "MIT License"
__version__     = "1.0.1"

# 01101100 00110000 00110000 01110000
__author__      = "Felix Geilert"


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='extensible-cache',
      version=__version__,
      description='Extensible Caching Framework for Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='cache;caching',
      url='https://github.com/felixnext/PythonCache',
      download_url='https://github.com/felixnext/PythonCache/archive/refs/tags/v1.0.1.tar.gz',
      author='Felix Geilert',
      license='MIT License',
      packages=find_packages(exclude=['tests*']),
      install_requires=['pandas'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      test_suite="tests",
      include_package_data=True,
      zip_safe=False)
