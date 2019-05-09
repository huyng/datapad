def _from_glob_paths(path_or_paths):
    """
    Construct a Sequence from file glob patterns

    Args:
        path_or_paths: str or list of strings
            A path, or list of paths. Paths may
            contain glob patterns like "data/metadata-*-a.txt"

    >>> seq = _from_glob_paths(["data/meta-*.txt"])
    >>> list(seq.all()) # doctest: +SKIP
    ["data/meta-1.json", "data/meta-2.json"]
    """

    if isinstance(path_or_paths, (tuple,list)):
        paths = path_or_paths
    else:
        paths = [path_or_paths]

    def _deglobify(path):
        import glob
        for p in glob.glob(path):
            yield p

    seq = Sequence.from_iterable(paths)
    seq = seq.flatmap(_deglobify)
    return seq

def read_text(path_or_paths, lines=True):
    """
    Construct a Sequence from text files

    Args:
        path_or_paths: str or list of strings
            A path, or list of paths. Paths may
            contain glob patterns like "data/metadata-*-a.txt"
        lines: bool
            If True, each element of the sequence comes from reading a line
            in the text file. If False, each element in sequence comes
            from the entire text file (default: True).

    >>> seq = read_text(["data/meta-*.txt"], lines=True)
    >>> list(seq.all()) # doctest: +SKIP
    ["foo_a", "foo_b", "bar_a", "bar_b"]

    >>> seq = read_text(["data/meta-*.txt"], lines=False)
    >>> list(seq.all()) # doctest: +SKIP
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
        lines: bool
            If True, each element of the sequence comes from decoding
            a line in the json-lines text file (see: http://jsonlines.org/examples/).
            If False, each element in sequence is obtained by running json.loads
            on the entire contents of the text file (default: True).
        ignore_errors: bool
            If True, ignore and skip over any elements that present json load errors

    >>> seq = read_json(["data/meta-*.json"], lines=True)
    >>> list(seq.all()) # doctest: +SKIP
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
        seq = seq.dropwhile(lambda v: v is None)

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
    >>> list(seq.all()) # doctest: +SKIP
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


class Sequence:

    def __init__(self, _iterable=None):
        self._iterable = _iterable if _iterable else []

    def map(self, fn):
        """
        Lazily apply fn function to every element of iterable

        Args:
            fn: function
                Function with signature fn(element) to apply to every
                element of sequence.


        >>> seq = Sequence.from_iterable(range(10))
        >>> seq = seq.map(lambda v: v*2)
        >>> list(seq.all())
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        """
        def _f(seq):
            for item in seq:
                yield fn(item)

        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def pmap_unordered(self, fn, workers=10):
        """
        Lazily apply fn function to every element of iterable, in parallel.
        The returned sequence may appear in a different order than the input
        sequence

        Args:
            fn: function
                Function with signature fn(element) -> element to apply to every
                element of sequence.
            workers: int
                Number of parallel processes to use (default: 10)

        >>> seq = Sequence.from_iterable(range(10))
        >>> seq = seq.map(lambda v: v*2)
        >>> list(seq.all()) # doctest: +SKIP
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 180]
        """
        from multiprocessing.dummy import Pool as ThreadPool
        pool = ThreadPool(workers)
        def _f(seq):
            for result in pool.imap_unordered(fn, seq):
                yield result

        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def flatmap(self, fn):
        """
        Lazily apply fn function to every element of iterable and chain the output
        into a single flattend sequence.

        Args:
            fn: function
                Function with signature fn(element) -> iterable(element) to apply to every
                element of sequence.


        >>> seq = Sequence.from_iterable(range(5))
        >>> seq = seq.flatmap(lambda v: [v,v])
        >>> list(seq.all())
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        """
        def _f(seq):
            for item in seq:
                for element in fn(item):
                    yield element
        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def filter(self, fn):
        """
        Lazily apply fn function to every element of iterable and keep only
        sequence elements where the function fn evaluates to True.

        Args:
            fn: function
                Function with signature fn(element) -> bool to apply to every
                element of sequence. Keep all elements in the sequence where the
                fn function evaluates to True.

        >>> seq = Sequence.from_iterable(range(5))
        >>> seq = seq.filter(lambda v: v > 1)
        >>> list(seq.all())
        [2, 3, 4]
        """

        def _f(seq):
            for item in seq:
                if fn(item) is not True:
                    continue
                yield item
        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def dropwhile(self, fn):
        """
        Lazily apply fn function to every element of iterable and drop
        sequence elements where the function fn evaluates to True.

        Args:
            fn: function
                Function with signature fn(element) -> bool to apply to every
                element of sequence. Drop all elements in the sequence where the
                fn function evaluates to True.

        >>> seq = Sequence.from_iterable(range(5))
        >>> seq = seq.dropwhile(lambda v: v > 1)
        >>> list(seq.all())
        [0, 1]
        """
        return self.filter(lambda v: not fn(v))

    def count(self):
        """
        Eagerly count number of elements in sequence

        >>> seq = Sequence.from_iterable(range(5))
        >>> seq.count()
        5
        """
        for i, _ in enumerate(self._iterable):
            pass
        return i+1

    def drop(self, count):
        """
        Lazily skip or drop over `count` elements.

        >>> seq = Sequence.from_iterable(range(5))
        >>> list(seq.all())
        [0, 1, 2, 3, 4]

        >>> seq = seq.drop(2)
        >>> list(seq.all())
        [2, 3, 4]
        """
        def _f(seq):
            for i, item in enumerate(seq):
                if i >= count:
                    yield item

        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def take(self, count):
        """
        Eagerly returns list of the first `count` elements.

        >>> seq = Sequence.from_iterable(range(5))
        >>> seq.take(2)
        [0, 1]
        """

        seq = self._iterable
        items = []
        for i, item in enumerate(seq):
            items.append(item)
            if (i+1) >= count:
                break
        return items

    def first(self):
        """
        Eagerly returns first element in sequence

        >>> seq = Sequence.from_iterable(range(5))
        >>> seq.first()
        0
        """

        return self.take(1)[0]

    def concat(self, seq):
        """
        Concatenates another sequence to the end
        of this sequence

        >>> seq = Sequence.from_iterable(range(5))
        >>> seq =seq.concat(seq)
        >>> list(seq.all())
        [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
        """

        import itertools as it
        if seq._iterable == self._iterable:
            a, b = it.tee(seq._iterable)
        else:
            a = self._iterable
            b = seq._iterable
        seq = Sequence(_iterable=it.chain(a, b))
        return seq

    def all(self):
        """
        Lazily returns all elements in sequence
        """
        return self._iterable

    @classmethod
    def from_iterable(cls, seq):
        """
        Construct a Sequence from any data type that follows
        the iterator API.

        >>> seq = Sequence.from_iterable([1,2,3])
        >>> list(seq.all())
        [1, 2, 3]
        """
        seq = cls(_iterable=seq)
        return seq



if __name__ == "__main__":
    import doctest
    doctest.testmod()
