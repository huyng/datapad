
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

class Tests(unittest.TestCase):

    def test_count(self):
        seq = sequence.Sequence([
            {'a': 1},
            {'b': 2}
        ])
        assert seq.count() == 2
