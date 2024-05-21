
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


class TestSinks(unittest.TestCase):

    def test_json_sink(self):
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile(delete=False) as fh:
            sink = io.JsonSink(fh.name, lines=True)
            seq = sequence.Sequence([1, 2, 3, 4, 5])
            seq.dump(sink)

            fh.seek(0)
            print(fh.read())

            sink = io.JsonSink(fh.name, append=True, lines=True)
            seq = sequence.Sequence([1, 2, 3, 4, 5])
            seq.dump(sink)

    def test_text_sink(self):
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile(delete=False) as fh:
            sink = io.TextSink(fh.name)
            seq = sequence.Sequence([1, 2, 3, 4, 5])
            seq.dump(sink)

            fh.seek(0)
            print(fh.read())

            sink = io.TextSink(fh.name, append=True)
            seq = sequence.Sequence([1, 2, 3, 4, 5])
            seq.dump(sink)


def example_processing_fn(v):
    return v*2


def test_pmap():

    # test thread-based parallel map
    seq = sequence.Sequence(range(1000))
    results = seq.pmap(lambda v: v*2, workers=4).collect()
    assert results == [v*2 for v in range(1000)], results

    # test process-based parallel map
    seq = sequence.Sequence(range(1000))
    results = seq.pmap(example_processing_fn,
                       workers=4,
                       wtype="process").collect()
    assert results == [v*2 for v in range(1000)], results
