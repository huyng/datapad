# Datapad

Datapad is a library for to processing sequence-based data using a [fluent API](https://en.wikipedia.org/wiki/Fluent_interface#Python). Think of it as an extended and chainable version of Python's `itertools` library.

This project incorporates ideas from:

* [LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/standard-query-operators-overview)
* [Spark](https://spark.apache.org/)
* [Python Itertools](https://docs.python.org/3/library/itertools.html)
* [Pandas](https://pandas.pydata.org/)
* [Dask](https://dask.org/)
* [Tensorflow tf.data.Datasets](https://www.tensorflow.org/api_docs/python/tf/data/Dataset)



### Install

```
pip install datapad
```

### Basic usage

create a sequence

```python
from datapad import Sequence
seq = Sequence(range(10))
```

map:

```python
seq = Sequence(range(10))
seq = seq.map(lambda v: v*2)
seq.collect()
```
```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```
filter:

```python
seq = Sequence(range(5))
seq = seq.filter(lambda v: v > 1)
seq.collect()
```

```
[2, 3, 4]
```
pmap_unordered:
```python
seq = Sequence(range(10))
seq = seq.map(lambda v: v*2)
seq.collect()
```
```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

flatmap:
```python
seq = Sequence(range(5))
seq = seq.flatmap(lambda v: [v,v])
seq.collect()
```
```
[0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
```

dropwhile:
```python
seq = Sequence(range(5))
seq = seq.dropwhile(lambda v: v > 1)
seq.collect()
```
```
[0, 1]
```

count:
```python
seq = Sequence(range(5))
seq.count()
```
```
5
```

drop:
```python
seq = Sequence(range(5))
seq = seq.drop(2)
seq.collect()
```
```
[2, 3, 4]
```

sort:
```python
seq = Sequence([2, 1, 0, 4, 3])
seq.sort().collect()
```

```
[0, 1, 2, 3, 4]
```


groupby:

```python
things = [("animal", "lion"),
          ("plant", "maple tree"),
          ("animal", "walrus"),
          ("plant", "grass")]
seq = Sequence(things)
groups = seq.sort().groupby(key=lambda x: x[0], getter=lambda x: x[1])
for key, group in groups:
   print(key, group)
```

```
animal ['lion', 'walrus']
plant ['grass', 'maple tree']
```


#### Operating on fields within a row of a Sequence

Suppose we have the following sequence

```python
seq = Sequence([
   {'a': 1},
   {'a': 2},
   {'a': 3}
])
```

Add fields:

```python
import datapad.fields as f
seq = seq.map(f.add({'b': lambda row: row['a'] + 3}))
seq.collect()
````

```
[
   {'a': 1, 'b': 4},
   {'a': 2, 'b': 5},
   {'a': 3, 'b': 6}
]
```

Apply functions to fields:

```python
import datapad.fields as f
seq = seq.map(f.apply({'a': lambda x: x*2)})
seq.collect()
````

```
[
   {'a': 2},
   {'a': 4},
   {'a': 6}
]
```

Select fields from a row:

```python
import datapad as dp
import datapad.fields as f
seq = dp.Sequence([{'a': 1, 'b': 2, 'c': 3}])
seq = seq.map(f.select(['a', 'c']))
seq.collect()
````

```
[
   {'a': 1, 'c': 3},
]
```
