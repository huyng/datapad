# datapad

### install

```
pip install datapad
```

### usage

create a sequence

```
from datapad import Sequence
seq = Sequence.from_iterable(range(10))
```

map:

```
seq = Sequence.from_iterable(range(10))
seq = seq.map(lambda v: v*2)
list(seq.all())
```
```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```
filter:

```
seq = Sequence.from_iterable(range(5))
seq = seq.filter(lambda v: v > 1)
list(seq.all())
```

```
[2, 3, 4]
```
pmap_unordered:
```
seq = Sequence.from_iterable(range(10))
seq = seq.map(lambda v: v*2)
list(seq.all()) # doctest: +SKIP
```
```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

flatmap:
```
seq = Sequence.from_iterable(range(5))
seq = seq.flatmap(lambda v: [v,v])
list(seq.all())
```
```
[0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
```

dropwhile:
```
seq = Sequence.from_iterable(range(5))
seq = seq.dropwhile(lambda v: v > 1)
list(seq.all())
```
```
[0, 1]
```

count:
```
seq = Sequence.from_iterable(range(5))
seq.count()
```
```
5
```

drop:
```
seq = Sequence.from_iterable(range(5))
seq = seq.drop(2)
list(seq.all())
```
```
[2, 3, 4]
```
