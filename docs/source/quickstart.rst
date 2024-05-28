===============
Getting started
===============

Overview
========

The central class in `datapad` is :class:`~datapad.Sequence` . This class provides an intuitive API for manipulating any sequence-like object using `fluent programming <https://en.wikipedia.org/wiki/Fluent_interface>`_. You can wrap python `lists`, `iterators`, `sets`, and `tuples` with this class to get access to all of the fluent-style APIs.

Let's begin by importing datapad::

    >>> import datapad as dp


Working with Sequences
======================

Creating a sequence is as simple as instantiating the `Sequence` class with any iterable data type. In the example below, we wrap a range iterator using the `Sequence` class::

    >>> seq = dp.Sequence(range(10))
    >>> seq
    <Sequence at 0x102983a5>

By default,  :class:`~datapad.Sequence` is "lazily" evaluated. This means a sequence will only return data when a result is requested. To evaluate a sequence to get a result, call the :func:`~datapad.Sequence.collect` method::

    >>> seq = dp.Sequence(range(10))
    >>> seq.collect()
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Most methods in :class:`~datapad.Sequence` are "chainable" (unless stated otherwise). That means the methods themselves return another :class:`~datapad.Sequence` object allowing you to easily chain multiple operations together like so::

    >>> seq = dp.Sequence(range(100))\
    ...         .map(lambda v: v*2)\
    ...         .keep_if(lambda v: (v%3) == 0))
    ...         .take(4)
    >>> seq.collect()
    [6, 12, 18, 24]

All :class:`~datapad.Sequence` objects conform to Python's iterator api, so you can manually iterate over them if you want to using a simple for-loop:

    >>> seq = dp.Sequence(range(10))
    >>> for elem in seq:
    ...     print(elem)

Of course, if you want a fluent-style API for code composability, try using datapad's native Sequence manipulation APIs below.


Slicing
-------

Sometimes you might not want to evaluate an entire sequence. For example, you might only want to evaluate the first element of a sequence. You can do so by calling the :func:`~datapad.Sequence.first` function::

    >>> seq = dp.Sequence(range(10))
    >>> seq.first() 0

Note, multiple calls to the :func:`~datapad.Sequence.first` function will advance the Sequence iterator::

    >>> seq = dp.Sequence(range(10))
    >>> seq.first()
    0
    >>> seq.first()
    1
    >>> seq.first()
    2


If you want to examine more than just the first element, you can call the :func:`~datapad.Sequence.take` function with a integer representing the number of items you want to evaluate from your Sequence::

    >>> seq = dp.Sequence(range(10))
    >>> seq.take(4).collect()
    [0, 1, 2, 3]

Alternatively, if you want to take a look at a sequence without advancing its underlying iterator you can use the :func:`~datapad.Sequence.peek` method::

    >>> seq = dp.Sequence(range(10))
    >>> seq.peek()
    0
    >>> seq.peek(4)
    [0, 1, 2, 3]
    >>> seq.peek(4)
    [0, 1, 2, 3]


Mapping over sequence
---------------------

The :class:`~datapad.Sequence` object in Datapad provides a variety of methods to transform the data in your sequence.

You can use the :func:`~datapad.Sequence.map` method to apply a function to every element in your sequence::

    >>> seq = dp.Sequence(range(10))
    >>> seq = seq.map(lambda elem: elem * 2)
    >>> seq.collect()
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

By default, most methods of the `Sequence` class returns a new sequence, enabling you to chain multiple :func:`~datapad.Sequence.map` calls together in order to process your data in multiple steps:

    >>> seq = dp.Sequence(range(3))
    >>> seq = seq.map(lambda elem: elem * 2)\
    ...          .map(lambda elem: (elem, elem))\
    ...          .collect()
    [(0, 0), (2, 2), (4, 4)]


Parallelized mapping
--------------------

If you have a IO or compute intensive map function, you can use :func:`~datapad.Sequence.pmap` to run your function in parallel using multiple worker threads or cpu processes::

    >>> def fetch_title(url):
    ...    import re
    ...    from urllib import request
    ...    contents = request.urlopen(url).read().decode("utf-8")
    ...    match = re.search('<title>(.*?)</title>', contents).groups()[0]
    ...    return match

    >>> urls = ["https://en.wikipedia.org/wiki/Vietnam",
    ...         "https://en.wikipedia.org/wiki/Da_Lat",
    ...         "https://en.wikipedia.org/wiki/Novak_Djokovic"]

    >>> seq = dp.Sequence(urls)
    >>> seq = seq.pmap(fetch_title, workers=2)
    >>> seq.collect()
    ['Vietnam - Wikipedia', 'Da Lat - Wikipedia', 'Novak Djokovic - Wikipedia']

In the code above, the function fetch\_title will run in two separate worker threads in parallel, pull down wikipedia content and parse out its title.

You can even get a progress bar for the above code by calling the :func:`~datapad.Sequence.progress` function before calling :func:`~datapad.Sequence.collect`::

    >>> seq.progress().collect()

Filtering elements
------------------

You can filter unwanted items from a sequence using the :func:`~datapad.Sequence.filter` method. This function takes as its arguments a single function that returns a boolean. All sequence elements that evaluate to `True` using this function will be returned, and all elements evaluating to `False` will be discarded::

    >>> seq = dp.Sequence(range(10))
    >>> seq = seq.filter(lambda elem: elem > 6)
    >>> seq.collect()
    [7, 8, 9]

You can use :func:`~datapad.Sequence.drop_if` to drop any sequence elements that match a given criteria::

    >>> seq = dp.Sequence(range(10))
    >>> seq.drop_if(lambda v: (v % 2) == 0).collect()
    [1, 3, 5, 7, 9]


Piping sequences
----------------

You can pipe your sequence to other functions for iterative processing using :func:`~datapad.Sequence.pipe`. These functions must take in a :class:`~datapad.Sequence` or Iterable as its first argument, and return another Sequence or iterable as its return value. We refer to these kinds of funcitons as "Pipes".


Similar to the concept of pipes on a unix command-line, piping allows you to seamlessly compose your :class:`~datapad.Sequence` code with pre-existing iteration functions. ::

    >>> def print_pipe(seq):
    ...     for elem in seq:
    ...         print("element: %d" % elem)
    ...         yield elem

    >>> dp.Sequence(range(5)).pipe(print_pipe).map(lambda v: v*2).collect()
    element: 0
    element: 1
    element: 2
    element: 3
    element: 4
    [0, 2, 4, 6, 8]

It can also be a useful tool to abstract out complicated sequence processing pipelines::

    >>> def my_pipe(seq):
    ...     seq = seq.drop_if(lambda v: v > 5)\
    ...              .map(lambda v: v*2)
    ...     return seq

    >>> seq = dp.Sequence(range(100))
    >>> seq.pipe(my_pipe).collect()
    [0, 2, 4, 6, 8, 10]

Counting
--------

You can count the number of elements with the :func:`~datapad.Sequence.count` method::

    >>> seq = dp.Sequence(range(10))
    >>> seq.count()
    10

Or you can count occurences of all distinct elements in your sequence::

    >>> seq = dp.Sequence(['a', 'a', 'b', 'b', 'b', 'c'])
    >>> seq.count(distinct=True).collect()
    [('a', 2), ('b', 3), ('c', 1)]

Sorting elements
----------------

Sort sequences using the :func:`~datapad.Sequence.sort` method.

    >>> seq = dp.Sequence([2,1, 5, 3])
    >>> seq = seq.sort()
    >>> seq.collect()
    [1, 2, 3, 5]

Grouping elements
-----------------

Group sequence elements togethering using the :func:`~datapad.Sequence.groupby` function. This function will return a sequence
of tuples where the first item is the key of the group and the second item is a list of items in the group. Note: the :func:`~datapad.Sequence.groupby`
function expects the sequence to be sorted to work properly::

    >>> seq = Sequence(['a', 'b', 'c', 'd', 'a', 'b', 'a', 'd'])
    >>> seq.sort().groupby(key=lambda x: x).collect()
    [
        ('a', ['a', 'a', 'a']),
        ('b', ['b', 'b']),
        ('c', ['c']),
        ('d', ['d', 'd']),
    ]

Discarding duplicates
---------------------

You can find all unique values in a `Sequence` by calling the :func:`~datapad.Sequence.distinct` function::

    >>> seq = Sequence(['a', 'b', 'c', 'd', 'a', 'b', 'a', 'd'])
    >>> seq.distinct().collect()
    ['a', 'b', 'c', 'd']


Joining sequences
-----------------

A common operation needed when working with messy data is to combine multiple sequences together based on a matching field. For example in the sequences below, we a presented with two sequences which are correlated using an ``id`` field. One sequence contains a person's name information and the other contains age information.

To match each element in each sequence to the same ``id``, we can use the :func:`~datapad.Sequence.join` function::

    >>> import datapad.fields as F
    >>> import datapad as dp
    >>> seq = dp.Sequence([
    ...     {'id': 1, 'name': 'John'},
    ...     {'id': 2, 'name': 'Nayeon'},
    ...     {'id': 3, 'name': 'Reza'}
    ... ])
    >>> other = dp.Sequence([
    ...     {'id': 1, 'age': 2},
    ...     {'id': 2, 'age': 3}
    ... ])
    >>> seq.join(other, key=F.get('id')).collect()
    [
        ({'id': 1, 'name': 'John'}, {'id': 1, 'age': 2}),
        ({'id': 2, 'name': 'Nayeon'}, {'id': 2, 'age': 3})
    ]

This function uses the ``key`` function ``F.get('id')`` (see :func:`datapad.fields.get` for more details) to match ids in sequence ``seq`` and ``other``. The result is a sequence of 2-tuples ``(a, b)`` where  ``a`` is an element in ``seq`` whose ``id`` matched element ``b`` in ``other``.

Note, any non-matching elements are simply discarded. This operation is commonly known in SQL terminology as an `inner` join.

If you'd would like a single, combined, dictionary instead of a sequence of 2-tuples, you can map a merging function over the resulting sequence::

    >>> import datapad.fields as F
    >>> import datapad as dp
    >>> seq = dp.Sequence([
    ...     {'id': 1, 'name': 'John'},
    ...     {'id': 2, 'name': 'Nayeon'},
    ...     {'id': 3, 'name': 'Reza'}
    ... ])
    >>> other = dp.Sequence([
    ...     {'id': 1, 'age': 2},
    ...     {'id': 2, 'age': 3}
    ... ])
    >>> seq.join(other, key=F.get('id'))\
    ...    .map(lambda d: dict(list(d[0].items()) + list(d[1].items())))\
    ...    .collect()
    [
        ({'id': 1, 'name': 'John',  'age': 2}),
        ({'id': 2, 'name': 'Nayeon', 'age': 3})
    ]


.. _structured-sequences:

Fields and Structured sequences
===============================

In nontrivial use-cases, `Sequences` are often made up of `Dictionaries`, `Lists`, or other container data-types. Datapad provides a set of functions in the :mod:`datapad.fields` module to work with these nested data types.

Combining this module along with  methods like :func:`datapad.Sequence.map` gives you a flexible and powerful framework for manipulating data sequences containing dictionaries and lists.

Below you'll find a few examples of working with sequences containing structured data. To begin, import the `fields` module::

    import datapad as dp
    import datapad.fields as F

Concepts
--------

* **Structured sequences** are simply `Sequences` that have `dicts` or `lists` as elements. These elements can be thought of as a `row` in a table.
* **Fields** are individual items within each `row`. They can be thought of as a `columns` in tabular data.
* A **field-key** is used to look up a specific **field-value** in a given `row` or `element` of a structured sequence.

    * When `elements` are `dicts`, a `field-key` refers to the dictionary key and a `field-value` refers to the corresponding dictionary value.
    * When `elements` are `lists`, a `field-key` refers to a specific index in the list and a `field-value` refers to the item at that list index.

Here's an example of a list-based structured sequence::

    >>> seq = dp.Sequence([
    ...     ['a', 1, 3],
    ...     ['b', 2, 3],
    ...     ['c', 3, 3]
    ... ])
    >>> seq.first()
    ['a', 1, 3]

Here's an example of a dict-based structure sequence::

    >>> seq = dp.Sequence([
    ...     {'a': 1, 'b': 2},
    ...     {'a': 4, 'b': 4},
    ...     {'a': 5, 'b': 7}
    ... ])
    >>> seq.first()
    {'a': 1, 'b': 2}



Selecting fields
----------------

You can retrieve individual fields within the elements of a structured sequence using the :func:`datapad.fields.select` function, which takes a list of keys for dict-based structured sequences::



    >>> seq = dp.Sequence([
    ...     {'a': 1, 'b': 2},
    ...     {'a': 4, 'b': 4},
    ...     {'a': 5, 'b': 7}
    ... ])
    >>> seq.map(F.select(['a'])).collect()
    [
        {'a': 1},
        {'a': 4},
        {'a': 5}
    ]

Or indices in the case of list-based structured sequences::

    >>> seq = dp.Sequence([
    ...     ['a', 1, 3],
    ...     ['b', 2, 3],
    ...     ['c', 3, 3]
    ... ])
    >>> seq.map(F.select([0, 2])).collect()
    [
        ['a', 3],
        ['b', 3],
        ['c', 3]
    ]

Transforming fields
-------------------

You can apply functions to individual fields using the :func:`datapad.fields.apply` function.

The simplest way to use this function is to pass it a field key or index and a function that will transform the field value::

    >>> seq = dp.Sequence([
    ...     {'a': 1, 'b': 2},
    ...     {'a': 4, 'b': 4},
    ...     {'a': 5, 'b': 7}
    ... ])
    >>> seq.map(F.apply('a', lambda x: x*2))\
    ...    .map(F.apply('b', lambda x: x*3))\
    ...    .collect()
    [
        {'a': 2, 'b': 6},
        {'a': 8, 'b': 12},
        {'a': 10, 'b': 21}
    ]

Adding fields
-------------

You can add fields using the :func:`datapad.fields.add` function.

The simplest way to use this function is to pass it a field key that you want to add and a function to generate a new field value. The function that you pass in must accept a the entire element and return a new value for the field. See below for an example::

    >>> seq = dp.Sequence([
    ...     {'a': 1, 'b': 2},
    ...     {'a': 4, 'b': 4},
    ...     {'a': 5, 'b': 7}
    ... ])
    >>> seq.map(F.add('c', lambda row: row['a'] + row['b']))\
    ...    .collect()
    [
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 4, 'b': 4, 'c': 8},
        {'a': 5, 'b': 7, 'c': 12}
    ]





