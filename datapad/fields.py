
# Copyright 2019 Huy Nguyen
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Software distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Functions for manipulating and retrieving fields within structured sequences.
These functions are often used in conjunction with the :func:`datapad.Sequence.map` method to
manipulate structured sequences.
"""

def asdict(keys=None):
    '''
    Constructs a function that will convert a list into a dict using the given
    keys. The returned function will have the signature::

        F(data:list) -> dict

    This function is commonly used in conjunction with :func:`datapad.Sequence.map`
    to manipulate structured sequence data.

    Args:
        keys (list):
            A list of strings or any other valid hashable type
            that will be associated with each element of the input
            ``data`` list. If `keys` is None, ``F(data)`` will use the
            indices of each list field as the key.

    Examples:

        Convert list to dict using pre-defined keys:

            >>> data = [1, 2, 3]
            >>> F = asdict(['a', 'b', 'c'])
            >>> F(data)
            {'a': 1, 'b': 2, 'c': 3}

        Convert list to dict using list indices as keys:

            >>> data = [1, 2, 3]
            >>> F = asdict()
            >>> F(data)
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
    Constructs a function to select fields from a list or dict.
    If a field-key is not present in data, default to None.

    Select from a list:

        >>> data = [1, 2, 3]
        >>> F = select([0, 2])
        >>> F(data)
        [1, 3]

    Select from a dictionary:

        >>> data = {'a': 2, 'b': 1, 'c': 4}
        >>> F = select(['c', 'b', 'k'])
        >>> F(data)
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
    Constructs a function to transform the fields in a dict or list of ``data``.
    The returned function will assume one of the following signatures::

        F(data:list) -> list
        F(data:dict) -> dict

    This function is commonly used in conjunction with :func:`datapad.Sequence.map`
    to manipulate structured sequence data.

    Possible ways to call the ``apply`` function::

        # apply func to all fields in data
        apply(func: Function)

        # apply func to data[key] field
        apply(key: Hashable, func: Function)

        # apply funcs[i] to data[i] fields
        apply(funcs: List[Function])

        # apply funcs[key] to data[key] fields
        apply(funcs: Dict[Hashable, Function])

    Args:
        key (string, int, hashable):
            A string, int, or other hashable value to be used to look up
            the field value to transform.

        func (function):
            A function that will take a single field value and transform it into a new value.

        funcs (List[Function], or Dict[Hashable, Function]):
            - If funcs is a list, ``F(data)`` will apply ``funcs[i]`` to ``data[i]``.
            - If funcs is a dict, ``F(data)`` will apply ``funcs[key]`` to ``data[key]``.
            - If a key in ``data`` has no corresponding key in ``funcs``, return the ``data[key]`` field untransformed.
            - If a key in ``funcs`` has no corresponding key in ``data``, abstain from applying ``funcs[key]``

    Examples:

        In the examples below, assume ``data`` represents a single row or element
        from a :class:`datapad.Sequence` object.

        Apply a single function to all fields:

            >>> data = [1, 2, 3]
            >>> F = apply(lambda x: x * 2)
            >>> F(data)
            [2, 4, 6]

        Apply a single function to a single field of a list
        (i.e. the value associated with the 2nd index):

            >>> data = [1, 2, 3]
            >>> F = apply(1, lambda x: x * 2)
            >>> F(data)
            [1, 4, 3]

        Apply a single function to a single field of a dict
        (i.e. the value associated with key 'a'):

            >>> data = {'a': 1, 'b': 2, 'c': 3}
            >>> F = apply('a', lambda x: x * 2)
            >>> F(data)
            {'a': 2, 'b': 2, 'c': 3}

        Apply multiple functions to several fields of a dict
        (i.e. the values associated with keys 'a', 'b', 'c', and 'd'):

            >>> data = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
            >>> F = apply({'a': lambda x: x*3, 'b': lambda x: 'foo'})
            >>> F(data)
            {'a': 3, 'b': 'foo', 'c': 3, 'd': 4}

        Apply multiple functions to several fields of a list
        (i.e. the values associated with index 0, and 1):

            >>> data = [1, 2, 3, 4]
            >>> F = apply({1: lambda x: x*3, 0: lambda x: 'foo'})
            >>> F(data)
            ['foo', 6, 3, 4]

        Apply multiple functions to several fields of a list
        (i.e. the values associated with index 0, and 1):

            >>> data = [1, 2, 3, 4]
            >>> F = apply([lambda x: x*2, lambda x: x*3])
            >>> F(data)
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
    Constructs a function to add or append new fields to a dict or list of ``data``.
    The returned function will assume one of the following signatures::

        F(data: list) -> list
        F(data: dict) -> dict

    This function is commonly used in conjunction with :func:`datapad.Sequence.map`
    to add new fields to structured sequence data.

    Possible ways to call the ``add`` function::

        # Append a single field with a value of `func(data)` to list `data`
        add(func: Function)

        # Add a single field to dict `data` by applying `data[key]` = `func(data)`
        add(key: Hashable, func: Function)

        # Append multiple fields with values [f(data) for f in funcs] to a list `data`
        add(funcs: List[func: Function])

        # Add multiple fields to a dict `data` by applying `data[key]` = `funcs[key](data)`
        add(funcs: Dict[key: Hashable, value: Function])

    Args:
        key (hashable):
            A string, int, or other hashable value to be used as the name of the
            added field.

        func (function):
            A function of the form ``f(data)`` to compute the value
            of the newly added element.

        funcs (List[Function], or Dict[Hashable, Function]):
            - If funcs is a list, ``data`` will be extended with values computed from ``f(data) for f in funcs``
            - If funcs is a dict, ``data[key]`` will be updated with values computed from ``funcs[key]``.
              Note: this will overwrite any existing keys with the same name in ``data``.


    Examples:

        In the examples below, assume ``data`` represents a single row or element
        from a :class:`datapad.Sequence` object.

        Add a single new element to end of list

            >>> data = [1, 2, 3]
            >>> F = add(lambda data: data[0] * data[1] * data[2])
            >>> F(data)
            [1, 2, 3, 6]

        Add a single new dictionary key and value:

            >>> data = {'a': 1, 'b': 2}
            >>> F = add('c', lambda data: data['a'] + data['b'])
            >>> F(data)
            {'a': 1, 'b': 2, 'c': 3}

        Add new dictionary keys:

            >>> data = {'a': 1, 'b': 2}
            >>> F = add({ 'c': (lambda data: data['a'] + data['b']), 'd': lambda data: 10})
            >>> F(data)
            {'a': 1, 'b': 2, 'c': 3, 'd': 10}

        Append new list elements:

            >>> data = ['foo', 'bar']
            >>> F = add([lambda data: data[1] + data[0]])
            >>> F(data)
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
