===============
Getting started
===============

Overview
========

The central class in `datapad` is ``datapad.Sequence`` . This class provides an intuitive API for manipulating any sequence-like object using `fluent programming <https://en.wikipedia.org/wiki/Fluent_interface>`_. You can wrap python `lists`, `iterators`, `sets`, and `tuples` with this class to get access to all of the fluent-style APIs.

Let's begin by importing datapad::

    >>> import datapad as dp


Creating Sequences
==================

Creating a sequence is as simple as instantiating the `Sequence` class with any iterable data type. In the example below, we wrap a range iterator using the `Sequence` class::

    >>> seq = dp.Sequence(range(10))
    >>> seq
    <Sequence at 0x102983a5>

By default, `Sequences` are "lazily" evaluated. This means a sequence will only return data when a result is requested. To evaluate a sequence to get a result, call the `collect` method::

    >>> seq = dp.Sequence(range(10))
    >>> seq.collect()
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Examining sequences
===================

Slicing
-------

Sometimes you might not want to evaluate an entire sequence. For example, you might only want to evaluate the first element of a sequence. You can do so by calling the `first` function::

    >>> seq = dp.Sequence(range(10))
    >>> seq.first()
    0

Note, multiple calls to the `first` function will advance the Sequence iterator::

    >>> seq = dp.Sequence(range(10))
    >>> seq.first()
    0
    >>> seq.first()
    1
    >>> seq.first()
    2

If you want to examine more than just the first element, you can call the `take` function with a integer representing the number of items you want to evaluate from your Sequence::

    >>> seq = dp.Sequence(range(10))
    >>> seq.take(4).collect()
    [0, 1, 2, 3]

Counting
--------

You can count the number of elements with the `count` method::

    >>> seq = dp.Sequence(range(10))
    >>> seq.count()
    10

Or you can count occurences of all distinct elements in your sequence::

    >>> seq = dp.Sequence(['a', 'a', 'b', 'b', 'b', 'c'])
    >>> seq.count(distinct=True).collect()
    [('a', 2), ('b', 3), ('c', 1)]


Manipulating sequences
======================

In addition to examining the data in a `Sequence` object, `Datapad` provides a variety of methods to transform the data in your sequence.

Transforming elements
---------------------

You can use the `map` method to apply function to every element in your sequence::

    >>> seq = dp.Sequence(range(10))
    >>> seq = seq.map(lambda elem: elem * 2)
    >>> seq.collect()
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

By default, most methods of the `Sequence` class returns a new sequence, enabling you to chain multiple `map` calls together in order to process your data in multiple steps:

    >>> seq = dp.Sequence(range(3))
    >>> seq = seq.map(lambda elem: elem * 2)\
    ...          .map(lambda elem: (elem, elem))\
    ...          .collect()
    [(0, 0), (2, 2), (4, 4)]

Filtering elements
------------------

You can filter unwanted items from a sequence using the `filter` method. This function takes as its arguments a single function that returns a boolean. All sequence elements that evaluate to `True` using this function will be returned, and all elements evaluating to `False` will be discarded::

    >>> seq = dp.Sequence(range(10))
    >>> seq = seq.filter(lambda elem: elem > 6)
    >>> seq.collect()
    [7, 8, 9]


Structured sequences
====================

In nontrivial use-cases, `Sequences` are often made up of `Dictionaries`, `Lists`, or other container data types. Datapad provides a set of convenience functions in the ``datapad.fields`` module to work with these data types.

Combining these methods along with the standard methods in the `Sequence` object gives you a flexible and powerful framework for manipulating data.

Below you'll find a few examples of working with sequences containing structured data. To begin, import the `fields` module::

    import datapad as dp
    import datapad.fields as F


What are structured sequences and fields?
-----------------------------------------

`Structured sequences` are simply `Sequences` that have `Dictionaries` or `Lists` as elements. `Fields` are individual items within each of element of a structured sequence.

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

You can retrieve individual fields within the elements of a structured sequence using the ``fields.select`` function, which takes a list of keys for dict-based structured sequences::



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

You can apply functions to individual fields using the ``fields.apply`` function.

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

You can add fields using the ``fields.add`` function.

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





