<!--
Copyright 2019 Huy Nguyen

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Software distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
-->

# Datapad: A Fluent API for Exploratory Data Analysis

[![Build Status](https://travis-ci.org/huyng/datapad.svg?branch=master)](https://travis-ci.org/huyng/datapad)
[![PyPI version](https://badge.fury.io/py/datapad.svg)](https://badge.fury.io/py/datapad)
[![Code Coverage](https://codecov.io/gh/huyng/datapad/branch/master/graph/badge.svg)](https://codecov.io/gh/huyng/datapad)

<p align="center">
  <img height="200" src="https://user-images.githubusercontent.com/121183/71599089-4cfe1080-2afe-11ea-8852-81f00ed8c3fa.jpg">
</p>

Datapad is a Python library for processing sequence and stream data using a [Fluent style API](https://en.wikipedia.org/wiki/Fluent_interface#Python). Data scientists and researchers use it as a lightweight toolset to efficiently explore datasets and to massage data for modeling tasks.

It can be viewed as a combination of syntatic sugar for Python's [itertools module](https://docs.python.org/3.8/library/itertools.html) and supercharged tools for working with [Structured Sequence](https://datapad.readthedocs.io/en/latest/quickstart.html#structured-sequences) data.

[Learn more in Documentation](https://datapad.readthedocs.io/en/latest/)

---

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

This project incorporates ideas from:

* [LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/standard-query-operators-overview)
* [Spark](https://spark.apache.org/)
* [Python Itertools](https://docs.python.org/3/library/itertools.html)
* [Pandas](https://pandas.pydata.org/)
* [Dask](https://dask.org/)
* [Tensorflow tf.data.Datasets](https://www.tensorflow.org/api_docs/python/tf/data/Dataset)
