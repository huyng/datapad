#!/usr/bin/env python

# Copyright(C) 2019 Huy Nguyen - All Rights Reserved

import os
os.environ['NOSE_DOCTEST_EXTENSION'] = 'txt'
os.environ['NOSE_WITH_DOCTEST'] = 'True'
os.environ['NOSE_WITH_DOCTESTS'] = 'True'
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='datapad',
    version='0.6.2',
    description='Datapad is a library of lazy data transformations for sequences; similar to spark and linq',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Huy Nguyen',
    author_email='',
    url='https://github.com/huyng/datapad',
    packages=['datapad'],
)
