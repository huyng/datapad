# Copyright(C) 2019 Huy Nguyen - All Rights Reserved

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
