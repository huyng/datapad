# Copyright(C) 2019 Huy Nguyen - All Rights Reserved
import collections


class Sequence:

    def __init__(self, _iterable=None):
        from collections.abc import Iterator

        _iterable = iter([]) if _iterable is None else _iterable

        # convert all iterables to iterator
        if not isinstance(_iterable, Iterator):
            _iterable = iter(_iterable)

        self._iterable = _iterable

    def map(self, fn):
        """
        Lazily apply fn function to every element of iterable

        Args:
            fn: function
                Function with signature fn(element) to apply to every
                element of sequence.


        >>> seq = Sequence(range(10))
        >>> seq = seq.map(lambda v: v*2)
        >>> seq.collect()
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        """
        def _f(seq):
            for item in seq:
                yield fn(item)

        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def reduce(self, fn, initial=None):
        """
        Eagerly apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
        ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
        of the sequence in the calculation, and serves as a default when the
        sequence is empty.

        Args:
            fn: function
                Function with signature fn(acc, current_item) -> acc_next
            initial: Any
                An initial value that acc will be set to. If not provided,
                this function will set the first element of the sequence as
                the initial value.

        >>> seq = Sequence(range(10))
        >>> seq.reduce(lambda acc, item: acc + item, initial=0)
        45
        """

        # if user provided initial value
        # use it as the first element passed to the reduce fn
        # otherwise use the first element of the iterable
        if initial is None:
            acc = next(self._iterable)
        else:
            acc = initial

        for item in self._iterable:
            acc = fn(acc, item)

        return acc

    def pmap(self, fn, workers=3, ordered=True):
        """
        Lazily apply fn function to every element of iterable, in parallel using
        multiprocess.dummy.Pool . The returned sequence may appear in a
        different order than the input sequence if you set `ordered` to False

        THIS FUNCTION IS EXPERIMENTAL

        Args:
            fn: function
                Function with signature fn(element) -> element to apply to every
                element of sequence.
            workers: int (default: 3)
                Number of parallel workers to use. These
                workers are implemented as python threads.
            ordered: bool (default: True)
                Whether to yield results in the same order in which items
                arrive. You may get better performance by setting this to false.

        >>> seq = Sequence(range(10))
        >>> seq = seq.pmap(lambda v: v*2)
        >>> seq.collect()
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

        >>> seq = Sequence(range(10))
        >>> seq = seq.pmap(lambda v: v*2, workers=1, ordered=False)
        >>> seq.collect()
        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        """
        from multiprocessing.dummy import Pool as ThreadPool
        pool = ThreadPool(workers)
        apply = pool.imap_unordered if not ordered else pool.imap

        def _f(seq):
            for result in apply(fn, seq):
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


        >>> seq = Sequence(range(5))
        >>> seq = seq.flatmap(lambda v: [v,v])
        >>> seq.collect()
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
        This is an alias for the Sequence.keep_if function

        >>> seq = Sequence(range(5))
        >>> seq = seq.filter(lambda v: v > 1)
        >>> seq.collect()
        [2, 3, 4]
        """
        return self.keep_if(fn)

    def keep_if(self, fn):
        """
        Lazily apply fn function to every element of iterable and keep only
        sequence elements where the function fn evaluates to True.

        Args:
            fn: function
                Function with signature fn(element) -> bool to apply to every
                element of sequence. Keep all elements in the sequence where the
                fn function evaluates to True.

        >>> seq = Sequence(range(5))
        >>> seq = seq.keep_if(lambda v: v > 1)
        >>> seq.collect()
        [2, 3, 4]
        """

        def _f(seq):
            for item in seq:
                if fn(item) is not True:
                    continue
                yield item
        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def drop_if(self, fn):
        """
        Lazily apply fn function to every element of iterable and drop
        sequence elements where the function fn evaluates to True.

        Args:
            fn: function
                Function with signature fn(element) -> bool to apply to every
                element of sequence. Drop all elements in the sequence where the
                fn function evaluates to True.

        >>> seq = Sequence(range(5))
        >>> seq = seq.drop_if(lambda v: v > 1)
        >>> seq.collect()
        [0, 1]
        """
        return self.filter(lambda v: not fn(v))

    def count(self, distinct=False):
        """
        Eagerly count number of elements in sequence

        Args:
            distinct: bool
                If True, counts occurence of each distinct
                value in sequence.
        Returns:
            Either an integer count or a new sequence of
            tuples where the first element is the unique value
            and the second element is the number of times
            that value appeared in the sequence.


        >>> seq = Sequence(range(5))
        >>> seq.count()
        5

        >>> seq = Sequence(['a', 'a', 'b', 'b', 'c', 'c'])
        >>> seq.count(distinct=True).collect()
        [('a', 2), ('b', 2), ('c', 2)]

        """

        counter = collections.Counter()
        for index, item in enumerate(self._iterable):
            counter[item] += 1

        if distinct:
            return Sequence(_iterable=counter.items())
        else:
            return index + 1

    def unique(self):
        """
        Eagerly returns a new sequence with unique values

        >>> seq = Sequence(['a', 'a', 'b', 'b', 'c', 'c'])
        >>> seq.unique().collect()
        ['a', 'b', 'c']
        """
        odict = collections.OrderedDict.fromkeys(list(self))
        return Sequence(_iterable=odict.keys())

    def zip_with_index(self):
        """
        Add an to each item in sequence

        >>> seq = Sequence(['a', 'b', 'c'])
        >>> seq.zip_with_index().collect()
        [(0, 'a'), (1, 'b'), (2, 'c')]
        """
        seq = Sequence(_iterable=enumerate(self._iterable))
        return seq

    def drop(self, count):
        """
        Lazily skip or drop over `count` elements.

        >>> seq = Sequence(range(5))
        >>> seq.collect()
        [0, 1, 2, 3, 4]

        >>> seq = Sequence(range(5))
        >>> seq = seq.drop(2)
        >>> seq.collect()
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
        Lazily returns a sequence of the first `count` elements.

        >>> seq = Sequence(range(5))
        >>> seq.take(2).collect()
        [0, 1]
        """
        def _f(seq):
            for i, item in enumerate(seq):
                yield item
                if (i + 1) >= count:
                    break

        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    def first(self):
        """
        Eagerly returns first element in sequence

        >>> seq = Sequence(range(5))
        >>> seq.first()
        0
        """
        items = self.take(1).collect()
        if len(items) == 0:
            return None
        return items[0]

    def concat(self, seq):
        """
        Concatenates another sequence to the end
        of this sequence

        >>> seq = Sequence(range(5))
        >>> seq =seq.concat(seq)
        >>> seq.collect()
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
        Returns a standard python iterator that you can
        use to lazily iterate over your sequence of data

        >>> seq = Sequence(range(10))
        >>> seq = seq.map(lambda v: v*2)
        >>> i = 0
        >>> for item in seq.all():
        ...     i += item
        >>> i
        90
        """
        return self._iterable

    def __iter__(self):
        """
        >>> seq = Sequence(range(10))
        >>> seq = seq.map(lambda v: v*2)
        >>> i = 0
        >>> for item in seq:
        ...     i += item
        >>> i
        90
        """

        return self.all()

    def collect(self):
        """
        Eagerly returns all elements in sequence

        >>> seq = Sequence(range(10))
        >>> seq.collect()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        return list(self.all())

    def sort(self, key=None):
        """
        Eagerly sorts your sequence and returns a
        newly created sequence containing the sorted items.
        WARNING: this function loads the entirety of your sequence
        into memory.

        >>> seq = Sequence([2, 1, 0, 4, 3])
        >>> seq.sort().collect()
        [0, 1, 2, 3, 4]
        """
        seq = Sequence(_iterable=sorted(list(self._iterable), key=key))
        return seq

    def groupby(self, key=None, getter=None, eager_group=True):
        """
        Groups sequence using key function,

        Note: you must ensure elements are sorted by groups before
        calling this function.

        Args:
            key: function
                Function used to determine what to use as a key for grouping

            getter: function
                Function to be applied to each element of a group

            eager_group: bool, default=True
                If true, eagerly convert a group from a lazy Sequence to
                a fully-realized list.


        >>> things = [("animal", "lion"), ("plant", "maple tree"), ("animal", "walrus"), ("plant", "grass")]
        >>> seq = Sequence(things)
        >>> groups = seq.sort().groupby(key=lambda x: x[0], getter=lambda x: x[1])
        >>> for key, group in groups:
        ...     print(key, group)
        animal ['lion', 'walrus']
        plant ['grass', 'maple tree']
        """
        if getter is None:
            def getter(x):
                return x

        def _f(iterable, key, getter):
            import itertools as it
            groups = it.groupby(iterable, key=key)

            for key, group in groups:
                group = (getter(element) for element in group)
                group_seq = Sequence(_iterable=group)

                if eager_group:
                    group_seq = group_seq.collect()

                yield key, group_seq

        seq = Sequence(_iterable=_f(self._iterable, key, getter))
        return seq

    def shuffle(self):
        """
        Eagerly shuffles your sequence and returns a
        newly created sequence containing the shuffled items.
        WARNING: this function loads the entirety of your sequence
        into memory.

        >>> import random
        >>> random.seed(0)
        >>> seq = Sequence(range(5))
        >>> seq.shuffle().collect()
        [2, 1, 0, 4, 3]
        """
        def _f(iterable):
            import random
            items = list(iterable)
            random.shuffle(items)
            return items
        seq = Sequence(_iterable=_f(self._iterable))
        return seq

    @classmethod
    def from_iterable(cls, iterable):
        """
        Construct a Sequence from any data type that follows
        the iterator API.

        >>> seq = Sequence([1,2,3])
        >>> seq.collect()
        [1, 2, 3]
        """
        seq = cls(_iterable=iterable)
        return seq


if __name__ == "__main__":
    import doctest
    doctest.testmod()
