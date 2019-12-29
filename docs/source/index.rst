.. Datapad documentation master file, created by
   sphinx-quickstart on Thu Dec 26 22:00:15 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/logo.png
    :width: 30%
    :align: center

|

==================================================
Datapad: Fluent APIs for Exploratory Data Analysis
==================================================


Datapad is a Python library for processing sequence-like data using a `fluent style API <https://en.wikipedia.org/wiki/Fluent_interface>`_. You can think of it as syntatic sugar for Python's ``itertools`` package (plus some additional goodies).

Datapad aims to optimize for developer happiness by providing an intuitive, consistent, and minimal API to manipulate a wide variety of data.

**Get Datapad**

Install datapad with the following command::

    pip install -U datapad

**Analyzing data with Datapad**

See what you can do with `datapad` in the examples below:


    >>> import datapad as dp
    >>> data = ['a', 'b', 'b', 'c', 'c', 'c']
    >>> seq = dp.Sequence(data)\
    ...         .distinct()\
    ...         .map(lambda x: x+'z')\
    ...         .map(lambda x: (x, len(x)))\
    ...         .collect()
    [('az', 2),
     ('bz', 2),
     ('cz', 2)]

    >>> import datapad as dp
    >>> data = ['a', 'b', 'b', 'c', 'c', 'c']
    >>> seq = dp.Sequence(data)\
    ...         .count(distinct=True)\
    ...         .collect()
    [('a', 1),
     ('b', 2),
     ('c', 3)]

    >>> import datapad as dp
    >>> import datapad.fields as F
    >>> data = [
    ...     {'a': 1, 'b': 2},
    ...     {'a': 4, 'b': 4},
    ...     {'a': 5, 'b': 7}
    ... ]
    >>> seq = dp.Sequence(data)
    >>> seq.map(F.apply('a', lambda x: x*2))\
    ...    .map(F.apply('b', lambda x: x*3))\
    ...    .collect()
    [{'a': 2, 'b': 6},
     {'a': 8, 'b': 12},
     {'a': 10, 'b': 21}]

For a more in-depth overview, see the "Getting Started" guide.

.. toctree::
    :maxdepth: 3
    :caption: The User Guide

    install
    quickstart
    reference

.. toctree::
    :caption: Additional Info
    :maxdepth: 1

    faq
    Source Code <https://github.com/huyng/datapad>


