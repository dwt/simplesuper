#!/usr/bin/env python
# encoding: utf-8
# from __future__ import unicode_literals

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='simplesuper',
    description='Simpler way to call super methods without all the repetition',
    long_description=open(os.path.join(here, 'Readme.md')).read(),
    long_description_content_type='text/markdown',
    version='1.0.10',
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
    py_modules=['simplesuper'],
    test_suite = "simplesuper",
)
