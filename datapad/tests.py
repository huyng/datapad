# Copyright(C) 2019 Huy Nguyen - All Rights Reserved

import unittest
import doctest
from . import sequence
from . import io
from . import fields

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(io))
    tests.addTests(doctest.DocTestSuite(sequence))
    tests.addTests(doctest.DocTestSuite(fields))
    return tests
