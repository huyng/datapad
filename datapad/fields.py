# Copyright(C) 2019 Huy Nguyen - All Rights Reserved


def asdict(keys=None):
    '''
    Returns a function that will convert
    lists to dicts, where keys are provided
    by `keys`. If `keys` is None, then use
    indices of list for keys.

    Convert list to dict using pre-defined keys:

        >>> data = [1, 2, 3]
        >>> asdict(['a', 'b', 'c'])(data)
        {'a': 1, 'b': 2, 'c': 3}

    Convert list to dict using list indices as keys:

        >>> data = [1, 2, 3]
        >>> asdict()(data)
        {0: 1, 1: 2, 2: 3}


    '''

    def _function(items):
        if keys is None:
            k = range(len(items))
        else:
            k = keys
        return dict(zip(k, items))
    return _function


# def aslist(keys=None):
#     '''
#     Returns a function that will convert
#     dicts to list, where keys are provided
#     by `keys`. If `keys` is None, then return
#     a list where elements are ordered by
#     their corresponding dictionary keys in
#     alphabetical order.

#     Convert list to dict using pre-defined keys:

#         >>> data = {'a': 1, 'b': 2, 'c': 3}
#         >>> asdict(['b', 'a', 'c'])(data)


#     Convert list to dict using list indices as keys:

#         >>> data = [1, 2, 3]
#         >>> asdict()(data)
#         {0: 1, 1: 2, 2: 3}
#     '''

#     def _function(items):
#         if keys is None:
#             k = range(len(items))
#         else:
#             k = keys
#         return dict(zip(k, items))
#     return _function


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


def apply(*args):
    '''
    Returns a function which transforms each element of `data` using the
    functions specified by `func` or `funcs`, in the following
    call signatures.

    Possible Call Signatures:
        apply(func:Function)
        apply(key:Hashable, func:Function)
        apply(funcs:List[func:Function])
        apply(funcs:Dict[key:Hashable, func:Function])

    Args:
        key:
            A string, int, or other hashable value to be used to look up
            the value to apply the transform to.
        func:
            Function of the form f(element: Any) -> Any to compute the value
            of the newly added element.

        funcs: function, list, or dict
            Functions must be of the form f(element: Any) -> Any.
            - If funcs is a single function, apply funcs to all elements in data.
            - If funcs is a list, apply funcs[i] to data[i].
            - If funcs is a dict, apply funcs[key] to data[key].
            - If a function in `funcs` does not exist for a key in data,
              return the data[key] untransformed.
            - Ignore any functions in funcs that don't have keys in data.

    Apply single function to all fields:

        >>> data = [1, 2, 3]
        >>> f = apply(lambda x: x * 2)
        >>> f(data)
        [2, 4, 6]

    Apply single function to a single field:

        >>> data = [1, 2, 3]
        >>> f = apply(1, lambda x: x * 2)
        >>> f(data)
        [1, 4, 3]

        >>> data = {'a': 1, 'b': 2, 'c': 3}
        >>> f = apply('a', lambda x: x * 2)
        >>> f(data)
        {'a': 2, 'b': 2, 'c': 3}

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

    if len(args) == 1:
        # if user passes in apply({'a': lambda d: 1})
        # or apply([lambda d: 1])
        if isinstance(args[0], (dict, list, tuple)):
            funcs = args[0]

        # if user passes in add(lambda d: 1)
        else:
            funcs = args[0]

    # if user passes in add('c', lambda d: 1)
    elif len(args) == 2:
        key = args[0]
        func = args[1]
        funcs = {key: func}
    else:
        raise ValueError('Please call add with one of the following signtures: (Function), (Str, Function), (List[Function]), or (Dict[Str, Function])')

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


def add(*args):
    '''
    Returns a function that when given a dict or list as `data` will add new keys
    or append new elements which are computed by applying functions
    in `funcs` to `data`.

    Possible Call Signatures:
        add(func:Function)
        add(key:Hashable, func:Function)
        add(funcs:List[func:Function])
        add(funcs:Dict[key:Hashable, func:Function])

    Args:
        key:
            A string, int, or other hashable value to be used as the name of the
            added field.
        func:
            Function of the form f(data:(List|Dict)) to compute the value
            of the newly added element.


    Add a single new element to end of list

        >>> data = [1, 2, 3]
        >>> f = add(lambda d: d[0]* d[1] * d[2])
        >>> f(data)
        [1, 2, 3, 6]

    Add a single new dictionary key and value:

        >>> data = {'a': 1, 'b': 2}
        >>> f = add('c', lambda d: d['a'] + d['b'])
        >>> f(data)
        {'a': 1, 'b': 2, 'c': 3}

    Add new dictionary keys:

        >>> data = {'a': 1, 'b': 2}
        >>> f = add({ 'c': (lambda d: d['a'] + d['b']), 'd': lambda d: 10})
        >>> f(data)
        {'a': 1, 'b': 2, 'c': 3, 'd': 10}

    Append new list elements:

        >>> data = ['foo', 'bar']
        >>> f = add([lambda d: d[1] + d[0]])
        >>> f(data)
        ['foo', 'bar', 'barfoo']

    '''

    if len(args) == 1:
        # if user passes in add({'a': lambda d: 1})
        # or add([lambda d: 1])
        if isinstance(args[0], (dict, list, tuple)):
            funcs = args[0]

        # if user passes in add(lambda d: 1)
        else:
            funcs = [args[0]]

    # if user passes in add('c', lambda d: 1)
    elif len(args) == 2:
        key = args[0]
        func = args[1]
        funcs = {key: func}
    else:
        raise ValueError('Please call add with one of the following signtures: (Function), (Str, Function), (List[Function]), or (Dict[Str, Function])')

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
