import unittest
import doctest
from . import sequence
from . import io

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(io))
    tests.addTests(doctest.DocTestSuite(sequence))
    return tests
