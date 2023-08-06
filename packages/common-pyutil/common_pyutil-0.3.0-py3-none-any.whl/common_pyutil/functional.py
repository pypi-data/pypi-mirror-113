from typing import Union, List, Optional, Any, Callable, Iterable, Dict
from functools import partial, reduce


def identity(x: Any):
    """Identity function.

    Example:
        identity(10) == 10
        identity(None) == None
    """
    return x


def rpartial(func, *args):
    def temp(*rest):
        return func(*rest, *args)
    return temp


def maybe_is(kinds: List[type], x: Any):
    return map(partial(apply, isinstance), [(x, k) for k in kinds])


def maybe_(kinds: List[type], x: Any):
    return last_item(first_by(zip(maybe_is(kinds, x), kinds), rpartial(nth, 0)))


def maybe_then(kinds: List[type], x: Any, then: List[Callable]):
    return last_item(first_by(zip(maybe_is(kinds, x), then), rpartial(nth, 0)))(x)


def foldl(func: Callable, struct: Iterable):
    it = iter(struct)
    yield(func(next(it)))


def first_by(struct: Optional[Iterable], by: Callable, predicate: Callable = identity):
    if struct:
        it = iter(struct)
        while True:
            try:
                x = next(it)
                if predicate(by(x)):
                    return x
            except StopIteration:
                return None


def last_item(struct: Optional[Iterable]):
    if struct:
        it = iter(struct)
        while True:
            try:
                x = next(it)
            except StopIteration:
                return x


def first(struct: Iterable, predicate: Callable = identity):
    """Return first item of `struct` which satisfies `predicate`.
    """
    return first_by(struct, identity, predicate)


def car(struct: Iterable):
    """Return first item of `struct`.
    """
    return next(iter(struct))


def first_item(struct: Iterable):
    """Return first item of `struct`.
    """
    return car(struct)


def nth(struct: Iterable, indx: int):
    it = iter(struct)
    i = 0
    x = None
    while i <= indx:
        try:
            x = next(it)
            i += 1
        except StopIteration:
            break
    return x


def applify(func: Callable, struct: Iterable[Iterable]):
    return map(partial(apply, func), struct)


def apply_list(funcs: Iterable[Callable], struct: Iterable) -> List:
    """Apply each function to item in two iterables.
    """
    return [fn(it) for fn, it in zip(funcs, struct)]


def apply(func: Callable, args: List):
    return func(*args)


def seq(*funcs: Callable) -> Callable:
    """Alias for thunkify
    """
    return thunkify(*funcs)


def pipe(*args: Callable) -> Callable:
    """Perform a function composition left to right.

    Example:
        def f(x: int):
            print(x)
            return str(x)

        def g(x: str):
            return "func g " + x

        def h(x: str):
            return "func h " + x

        pipe(f, g, h)(10)   # prints 10 and returns "func h func g 10"

    """
    return partial(reduce, lambda x, y: y(x), args)


def compose(*args: Callable) -> Callable:
    """Perform a function composition right to left."""
    return partial(reduce, lambda x, y: y(x), args[::-1])


def thunkify(*args: Callable) -> Callable:
    """Creates a thunk out of a function.

    A thunk delays a calculation until its result is needed, providing lazy
    evaluation of arguments. Can be used for side effects.

    Example:
        def f(x: int):
            print("func f", x)

        def g():
            print("func g")

        val = 10
        thunk = thunkify(partial(f, val), g)
        thunk()   # prints "func f 10" and "func g"

        # Or if val won't be available till later
        thunk = thunkify(f, lambda *_: g())
        some_other_func(arg1, arg2, thunk)

        # In some_other_func
        val = 20
        thunk(val)   # prints "func f 20" and "func g"

    """
    def thunk(*_args):
        for a in args:
            a(*_args)
    return thunk


def print_lens(obj: Optional[Dict], *args, prefix="") -> Any:
    """Return a value in a nested object and also print it.

    Like :func:`lens` but with more feedback
    """
    if obj is None:
        print(prefix + " (NOT FOUND)")
        return None
    elif args:
        return print_lens(obj.get(args[0]), *args[1:],
                          prefix=(prefix + " -> " if prefix else "") + str(args[0]))
    else:
        print(prefix + " -> " + str(obj))
        return obj


def set_lens(obj: Optional[Dict], keys: List[str], val: Any) -> bool:
    """Return a value in a nested object.
    """
    if obj is None:
        return False
    elif keys and len(keys) == 1:
        obj[keys[0]] = val
        return True
    elif keys:
        return set_lens(obj.get(keys[0]), keys[1:], val)
    else:
        return False


def lens(obj: Optional[Dict], *args) -> Any:
    """Return a value in a nested object.
    """
    if obj is None:
        return None
    elif args:
        return lens(obj.get(args[0]), *args[1:])
    else:
        return obj


def difference(a: Iterable, b: Iterable) -> set:
    """Return set difference of two iterables"""
    a = set([*a])
    b = set([*b])
    return a - b


def intersection(a: Iterable, b: Iterable) -> set:
    """Return intersection of two iterables"""
    a = set([*a])
    b = set([*b])
    return a.intersection(b)


def union(a: Iterable, b: Iterable) -> set:
    """Return union of two iterables"""
    a = set([*a])
    b = set([*b])
    return a.union(b)


def concat(list_var: Iterable[List]) -> List:
    """Concat all items in a given list of lists"""
    temp = []
    for x in list_var:
        temp.extend(x)
    return temp


def takewhile(predicate, seq):
    """Lazily evaluated takewhile

    :param predicate: First failure of predicate stops the iteration. Should return bool
    :param seq: Sequence from which to take
    :returns: filtered sequence
    :rtype: Same as `seq`

    """
    it = iter(seq)
    _next = it.__next__()
    while predicate(_next):
        try:
            yield _next
            _next = it.__next__()
        except StopIteration:
            return None


def flatten_struct(struct, _type=None):
    """Return a flattend list from a possibly nested iterable.

    I'm not sure there's a usecase for this beyond lists
    """
    retval = []
    # in case the underlying structure is also an iterable to avoid that also
    # being extended with retval, e.g., a string
    t = _type or type(struct)
    it = iter(struct)
    _next = it.__next__()
    while _next:
        try:
            if not isinstance(_next, t):
                retval.append(_next)
            else:
                retval.extend(flatten(_next, t))
            _next = it.__next__()
        except StopIteration:
            return retval
    return retval


def flatten(_list: List, depth: Optional[int] = None):
    """Return a flattend list from a possibly nested list.

    Args:
        depth: Depth to recurse
    """
    retval = []
    if depth is not None:
        depth -= 1
        if depth == -1:
            return _list
    for x in _list:
        if not isinstance(x, list):
            retval.append(x)
        else:
            retval.extend(flatten(x, depth))
    return retval


def map_if(func: Callable, pred: Callable[..., bool], struct: Iterable) -> list:
    """Map :code:`func` to :code:`struct` if item of :code:`struct` satisfies :code:`pred`

    Args:
        func: Any Callable
        pred: A predicate which returns a bool
        struct: Iterable on which to map
    """
    retval = []
    it = iter(struct)
    _next = it.__next__()
    while _next:
        try:
            retval.append(func(_next) if pred(_next) else _next)
            _next = it.__next__()
        except StopIteration:
            return retval
    return retval
