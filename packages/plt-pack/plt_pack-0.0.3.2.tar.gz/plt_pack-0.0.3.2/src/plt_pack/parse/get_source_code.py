from inspect import getsource
from functools import partial
from types import FunctionType


def get_source_code(func: FunctionType or partial) -> str:
    """
    Parse source code with fixed indentations, omitted decorators and partial.

    Args:
        func (FunctionType): A target function to parse.

    Returns:
        str: Source code with fixed indentations and omitted decorators.

    Examples:
        >>> def decorator(fun):
        ...     return fun
        ...
        >>> print(get_source_code(decorator).rstrip())
        def decorator(fun):
            return fun

        >>> def parent_func():
        ...     def nested_func(*args, **kwargs):
        ...         pass
        ...     return nested_func
        ...
        >>> print(get_source_code(parent_func).rstrip())
        def parent_func():
            def nested_func(*args, **kwargs):
                pass
            return nested_func

        >>> print(get_source_code(parent_func()).rstrip())
        def nested_func(*args, **kwargs):
            pass

        >>> @decorator
        ... def func():
        ...     pass
        ...
        >>> print(get_source_code(func).rstrip())
        def func():
            pass

        >>> print(get_source_code(partial(decorator, func)).rstrip())
        def decorator(fun):
            return fun



    """
    if isinstance(func, partial):
        func = func.func
    src = getsource(func)
    src = _fix_func_code(src)
    return src


def _fix_func_code(func_code: str):
    func_code = _fix_indents(func_code, ' ')
    func_code = _fix_indents(func_code, '\t')
    func_code = _remove_decorators(func_code)

    return func_code


def _remove_decorators(func_code: str):
    counts = 0
    lines = func_code.split('\n')

    for line in lines:
        if line.startswith('def '):
            break
        counts += 1
    return '\n'.join(lines[counts:])


def _fix_indents(func_code: str, char: str):
    counts: int = 0
    lines = func_code.split('\n')

    for ch in lines[0].split(char):
        if ch:
            break
        counts += 1
    return '\n'.join([line[counts:] for line in lines])
