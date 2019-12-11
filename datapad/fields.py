# Copyright(C) 2019 Huy Nguyen - All Rights Reserved

def asdict(keys=None):
    '''
    Returns a function that will convert
    lists to dicts, where keys are provided
    by `keys`. If `keys` is None, then use
    indices of list for keys.

    >>> data = [1, 2, 3]
    >>> asdict(['a', 'b', 'c'])(data)
    {'a': 1, 'b': 2, 'c': 3}

    '''

    def _function(items):
        if keys is None:
            k = range(len(items))
        else:
            k = keys
        return dict(zip(k, items))
    return _function


def select(keys):
    '''
    Returns a function to select
    keys from a list or dict. If key is not
    present in data, default to None.

    Select from a list:

        >>> data = [1, 2, 3]
        >>> select([0, 2])(data)
        [1, 3]

    Select from a dictionary:

        >>> data = {'a': 2, 'b': 1, 'c': 4}
        >>> select(['c', 'b', 'k'])(data)
        {'c': 4, 'b': 1, 'k': None}

    '''
    def _function(items):
        if isinstance(items, list):
            new_items = []
            total_items = len(items)
            for key in keys:
                if key >= total_items:
                    new_items.append(None)
                else:
                    new_items.append(items[key])

        elif isinstance(items, dict):
            new_items = {}
            for key in keys:
                if key not in items:
                    new_items[key] = None
                else:
                    new_items[key] = items[key]
        return new_items
    return _function


def apply(funcs):
    '''
    Returns a function of the form

        f(data: list) -> list
        f(data: dict) -> dict

    which transforms each element of `data` using the
    functions specified in `funcs`.

    Args:
        funcs: function, list, or dict
            Functions must be of the form f(element: Any) -> Any.
            - If funcs is a single function, apply funcs to all elements in data.
            - If funcs is a list, apply funcs[i] to data[i].
            - If funcs is a dict, apply funcs[key] to data[key].
            - If a function in `funcs` does not exist for a key in data,
              return the data[key] untransformed.
            - Ignore any functions in funcs that don't have keys in data.

    Apply single function:

        >>> data = [1, 2, 3]
        >>> f = apply(lambda x: x * 2)
        >>> f(data)
        [2, 4, 6]

    Apply a dict of functions:

        >>> data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        >>> f = apply({'a': lambda x: x*3, 'b': lambda x: 'foo'})
        >>> f(data)
        {'a': 3, 'b': 'foo', 'c': 3, 'd': 4}

        >>> data = [1, 2, 3, 4]
        >>> f = apply({1: lambda x: x*3, 0: lambda x: 'foo'})
        >>> f(data)
        ['foo', 6, 3, 4]

    Apply a list of functions:

        >>> data = [1, 2, 3, 4]
        >>> f = apply([lambda x: x*2, lambda x: x*3])
        >>> f(data)
        [2, 6, 3, 4]


    '''

    # convert funcs to a dict if passed in as a list
    if isinstance(funcs, list):
        funcs = dict(zip(range(len(funcs)), funcs))

    def _function(data):

        if isinstance(data, list):
            new_data = []
            for key, value in enumerate(data):
                if not isinstance(funcs, (list, dict)):
                    f = funcs
                    new_data.append(f(value))
                elif key not in funcs:
                    new_data.append(value)
                else:
                    f = funcs[key]
                    new_data.append(f(value))

        elif isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                if not isinstance(funcs, (list, dict)):
                    f = funcs
                    new_data[data] = f(value)
                elif key not in funcs:
                    new_data[key] = value
                else:
                    f = funcs[key]
                    new_data[key] = f(value)
        return new_data

    return _function


def add(funcs):
    '''
    Returns a function that given a dict or list as `data` will add new keys
    or append new elements which are computed by applying functions
    in `funcs` to `data`.

    Args:
        funcs: list or dict
            Functions must take the form f(data: [list, dict]) -> Any

    Add new dictionary keys:

        >>> data = {'a': 1, 'b': 2}
        >>> f = add({ 'c': (lambda d: d['a'] + d['b']) })
        >>> f(data)
        {'a': 1, 'b': 2, 'c': 3}

    Append new list elements:

        >>> data = ['foo', 'bar']
        >>> f = add([lambda d: d[1] + d[0]])
        >>> f(data)
        ['foo', 'bar', 'barfoo']

    '''

    def _function(data):
        if isinstance(data, list):
            new_data = []
            for f in funcs:
                new_data.append(f(data))
            return data + new_data

        elif isinstance(data, dict):
            new_data = {}
            new_data.update(data)
            for key, f in funcs.items():
                new_data[key] = f(data)
            return new_data

    return _function


if __name__ == "__main__":
    import doctest
    doctest.testmod()
