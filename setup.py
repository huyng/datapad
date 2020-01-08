#!/usr/bin/env python

# Copyright 2019 Huy Nguyen
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Software distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

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
    version='0.6.7',
    description='Datapad is a library of lazy data transformations for sequences; similar to spark and linq',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Huy Nguyen',
    author_email='',
    url='https://github.com/huyng/datapad',
    packages=['datapad'],
)
