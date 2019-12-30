

# Datapad: A Fluent API for Exploratory Data Analysis

[![Build Status](https://travis-ci.org/huyng/datapad.svg?branch=master)](https://travis-ci.org/huyng/datapad)
[![PyPI version](https://badge.fury.io/py/datapad.svg)](https://badge.fury.io/py/datapad)
[![Code Coverage](https://codecov.io/gh/huyng/datapad/branch/master/graph/badge.svg)](https://codecov.io/gh/huyng/datapad)

<p align="center">
  <img height="200" src="https://user-images.githubusercontent.com/121183/71599089-4cfe1080-2afe-11ea-8852-81f00ed8c3fa.jpg">
</p>

Datapad is a Python library for processing sequence and stream data using a [Fluent style API](https://en.wikipedia.org/wiki/Fluent_interface#Python). Data scientists and researchers use it as a lightweight toolset to efficiently explore datasets and to massage/clean data for modeling tasks.

You can think of it as syntatic sugar for Python’s itertools module (plus some additional goodies).

### Install

```
pip install datapad
```

### Exploratory data analysis with Datapad

See what you can do with `datapad` in the examples below:

```python
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
```

```python
>>> import datapad as dp
>>> data = ['a', 'b', 'b', 'c', 'c', 'c']
>>> seq = dp.Sequence(data)
>>> seq.count(distinct=True) \
...    .collect()
[('a', 1),
 ('b', 2),
 ('c', 3)]
```

```python
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
```

This project incorporates ideas from:

* [LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/standard-query-operators-overview)
* [Spark](https://spark.apache.org/)
* [Python Itertools](https://docs.python.org/3/library/itertools.html)
* [Pandas](https://pandas.pydata.org/)
* [Dask](https://dask.org/)
* [Tensorflow tf.data.Datasets](https://www.tensorflow.org/api_docs/python/tf/data/Dataset)
