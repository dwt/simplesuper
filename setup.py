#!/usr/bin/env python
# encoding: utf-8
# from __future__ import unicode_literals

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

setup(
    name='simplesuper',
    description=open(path.join(here, 'Readme.md')).read(),
    version='1.0.5',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: ISC License (ISCL)",
    ],
    author='Martin Häcker, Robert Buchholz, Felix Schwarz',
    author_email='mhaecker@mac.com, rbu@rbu.sh, felix@schwarz-online.org',
    license="ISC",
    url='https://github.com/dwt/simplesuper',
    keywords='python 2, super, convenience, api',
    include_package_data = True,
    package_data = {
        '': ['*.txt', '*.md'],
    },
    py_modules=['simple_super'],
    test_suite = "simple_super",
    zip_safe=True,
)
