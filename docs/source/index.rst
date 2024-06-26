.. Datapad documentation master file, created by
   sphinx-quickstart on Thu Dec 26 22:00:15 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/logo.jpg
  :height: 170
  :alt: Datapad Logo
  :align: center

|

Datapad - Data processing & analysis with chainable fluent APIs
===============================================================

Datapad is a Python library for processing sequence and stream data using a `Fluent style API <https://en.wikipedia.org/wiki/Fluent_interface>`_. Data scientists and researchers use it as a lightweight toolset to efficiently explore datasets and to massage data for modeling tasks.

It can be viewed as lightweight syntatic sugar for Python's `itertools <https://docs.python.org/3.8/library/itertools.html>`_ module and supercharged tooling for working with :ref:`structured-sequences`. It is modeled similarly to Microsoft .NET's Linq system.

Datapad optimizes for developer happiness by providing an intuitive, consistent, and minimal API to manipulate a wide variety of data.

Getting Datapad
---------------

Install datapad with the following command::

    pip install -U datapad

Exploratory data analysis with Datapad
--------------------------------------

See what you can do with `datapad` in the examples below.


**Count all unique items in a sequence:**

    >>> import datapad as dp
    >>> data = ['a', 'b', 'b', 'c', 'c', 'c']
    >>> seq = dp.Sequence(data)
    >>> seq.count(distinct=True) \
    ...    .collect()
    [('a', 1),
     ('b', 2),
     ('c', 3)]

**Transform individual fields in a sequence:**

    >>> import datapad as dp
    >>> import datapad.fields as F
    >>> data = [
    ...     {'a': 1, 'b': 2},
    ...     {'a': 4, 'b': 4},
    ...     {'a': 5, 'b': 7}
    ... ]
    >>> seq = dp.Sequence(data)
    >>> seq.map(F.apply('a', lambda x: x*2)) \
    ...    .map(F.apply('b', lambda x: x*3)) \
    ...    .collect()
    [{'a': 2, 'b': 6},
     {'a': 8, 'b': 12},
     {'a': 10, 'b': 21}]

**Chain together multiple transforms for the elements of a sequence:**

    >>> import datapad as dp
    >>> data = ['a', 'b', 'b', 'c', 'c', 'c']
    >>> seq = dp.Sequence(data)
    >>> seq.distinct() \
    ...    .map(lambda x: x+'z') \
    ...    .map(lambda x: (x, len(x))) \
    ...    .collect()
    [('az', 2),
     ('bz', 2),
     ('cz', 2)]

For a more in-depth overview, see the "Getting Started" guide.

.. toctree::
    :maxdepth: 3
    :caption: The User Guide

    Home <https://datapad.readthedocs.io/en/latest/>
    install
    quickstart
    reference

.. toctree::
    :caption: Additional Info
    :maxdepth: 1

    faq
    Source Code <https://github.com/huyng/datapad>



