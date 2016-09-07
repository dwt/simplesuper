#!/usr/bin/env python
# encoding: utf-8
# from __future__ import unicode_literals

from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

def readme():
    "Falls back to just file().read() on any error, because the conversion to rst is only really relevant when uploading the package to pypi"
    from subprocess import CalledProcessError
    try:
        from subprocess import check_output
        return str(check_output(['pandoc', '--from', 'markdown', '--to', 'rst', 'README.md']))
    except (ImportError, OSError, CalledProcessError) as error:
        print('python2.6 and pandoc is required to get the description as rst (as required to get nice rendering in pypi) - using the original markdown instead.',
              'See http://johnmacfarlane.net/pandoc/')
    return str(open(path.join(here, 'Readme.md')).read())


setup(
    name='simplesuper',
    description='Simpler way to call super methods without all the repetition',
    long_description=readme(),
    version='1.0.9',
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
