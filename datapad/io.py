
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

"""
Convenience functions for creating Sequences from files and other input sources.
"""

from .sequence import Sequence


def _from_glob_paths(path_or_paths):
    """
    Construct a Sequence from file glob patterns

    Args:
        path_or_paths: str or list of strings
            A path, or list of paths. Paths may
            contain glob patterns like "data/metadata-*-a.txt"

    >>> seq = _from_glob_paths(["data/meta-*.txt"])
    >>> seq.collect() # doctest: +SKIP
    ["data/meta-1.json", "data/meta-2.json"]
    """

    if isinstance(path_or_paths, (tuple, list)):
        paths = path_or_paths
    else:
        paths = [path_or_paths]

    def _deglobify(path):
        # todo make sure we only deglobify if path is glob
        import glob
        for p in glob.glob(path):
            yield p

    seq = Sequence(paths)
    seq = seq.flatmap(_deglobify)
    return seq


def read_text(path_or_paths, lines=True):
    """
    Construct a Sequence from text files

    Args:
        path_or_paths: str or list of strings
            A path, or list of paths. Paths may
            contain glob patterns like "data/metadata-*-a.txt"
        lines: bool (default: True)
            If True, each element of the sequence comes from reading a line
            in the text file. If False, each element in sequence comes
            from the entire text file.

    >>> seq = read_text(["data/meta-*.txt"], lines=True)
    >>> seq.collect() # doctest: +SKIP
    ["foo_a", "foo_b", "bar_a", "bar_b"]

    >>> seq = read_text(["data/meta-*.txt"], lines=False)
    >>> seq.collect() # doctest: +SKIP
    ["foo_a\\nfoo_b", "bar_a\\nbar_b"]
    """

    def _read(path):
        with open(path) as fh:
            # read each file as a sequence of lines
            # otherwise read each file a single single string
            if lines:
                for line in fh:
                    yield line
            else:
                yield fh.read()

    seq = _from_glob_paths(path_or_paths)
    seq = seq.flatmap(_read)
    return seq


def read_json(path_or_paths, lines=True, ignore_errors=False):
    """
    Construct a Sequence from json text files

    Args:
        path_or_paths: str or list of strings
            A path, or list of paths. Paths may
            contain glob patterns like "data/metadata-*-a.txt"
        lines: bool (default: True)
            If True, each element of the sequence comes from decoding
            a line in the json-lines text file (see: http://jsonlines.org/examples/).
            If False, each element in sequence is obtained by running json.loads
            on the entire contents of the text file .
        ignore_errors: bool
            If True, ignore and skip over any elements that present json load errors

    >>> seq = read_json(["data/meta-*.json"], lines=True)
    >>> seq.collect() # doctest: +SKIP
    [{"dog": 1}, {"dog": 2}]
    """
    import json

    seq = read_text(path_or_paths, lines=lines)
    if ignore_errors:

        def maybe_json_loads(s):
            try:
                return json.loads(s)
            except json.JSONDecodeError:
                return None

        seq = seq.map(maybe_json_loads)
        seq = seq.drop_if(lambda v: v is None)

    else:
        seq = seq.map(json.loads)
    return seq


def read_csv(path_or_paths):
    """
    Construct a Sequence from json text files

    Args:
        path_or_paths: str or list of strings
            A path, or list of paths. Paths may
            contain glob patterns like "data/metadata-*-a.txt"

    >>> seq = read_csv(["data/meta-*.csv"])
    >>> seq.collect() # doctest: +SKIP
    [["foo", "bar"],
     ["1", "2"],
     ["3", "4"]]
    """

    def _read(path):
        import csv
        with open(path, newline="") as fh:
            dialect = csv.Sniffer().sniff(fh.read(1024))
            fh.seek(0)
            reader = csv.reader(fh, dialect)
            for row in reader:
                yield row

    seq = _from_glob_paths(path_or_paths)
    seq = seq.flatmap(_read)
    return seq


# ------------------------------------------------
# Sinks Are Callables that will consume a sequence
# ------------------------------------------------

class JsonSink:
    def __init__(self,
                 path: str,
                 lines: bool = True,
                 append: bool = False,
                 ignore_errors: bool = False,
                 verbose: bool = True):
        """
        A JSON sink for JSON writing

        Args:
            path: str
                A path to the JSON file you want to write
            lines: bool (default: True)
                If True, each element of the sequence comes will be encoded
                and written to a single line to the json-lines text file
                (see: http://jsonlines.org/examples/).  If False, aggregate
                the entire sequence into a single array and write array to the
                target file path.
            append: bool (default: False)
                If True, append to the target file rather than overwriting target
                file if it already exists.
            ignore_errors: bool (default: False)
                If True, ignore and skip over any elements that present json
                encoding errors
            verbose: bool (default: True)
                If True, report number of records processed
        """

        self.lines = lines
        self.path = path
        self.ignore_errors = ignore_errors
        self.append = append
        self.verbose = verbose

    def __call__(self, seq):
        import json

        # re-assign seq, so that it produces a progress output
        if self.verbose:
            seq = seq.progress()

        mode = "a" if self.append else "w"
        with open(self.path, mode) as fh:

            # if not json lines format, just write entire file
            # as a aggregated list
            if not self.lines:
                json.dump(seq.collect(), fh)
                return

            # begin writing json
            if self.ignore_errors:
                for i, elem in enumerate(seq):
                    try:
                        j = json.dumps(elem)
                        fh.write(j+'\n')
                    except Exception:
                        continue
            else:
                for i, elem in enumerate(seq):
                    j = json.dumps(elem)
                    fh.write(j+'\n')

        if self.verbose:
            print("")


class TextSink:
    def __init__(self,
                 path: str,
                 append: bool = False,
                 verbose: bool = True):
        """
        A Text sink for writing lines of strings to a textfile

        Args:
            path: str
                A path to the text file you want to write
            append: bool (default: False)
                If True, append to the target file rather than
                overwriting target file if it already exists.
            verbose: bool (default: True)
                If True, report number of records processed
        """
        self.path = path
        self.append = append
        self.verbose = verbose

    def __call__(self, seq):
        # re-assign seq, so that it produces a progress output
        # if user requests
        if self.verbose:
            seq = seq.progress()

        mode = "a" if self.append else "w"
        with open(self.path, mode) as fh:

            # begin writing json
            for elem in seq:
                fh.write(str(elem) + '\n')

        if self.verbose:
            print("")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
