import ast

from typing import Any
from functools import partial
from types import FunctionType

from .get_source_code import get_source_code

__all__ = ['get_real_func_name']


def get_real_func_name(fun: FunctionType or partial) -> str:
    """
    Parses a function and returns its 'real' name from its code.

    Args:
        fun (FunctionType): A target function.

    Returns:
        str: Function's parsed name.

    >>> def func_1(*args):
    ...     pass
    ...
    >>> get_real_func_name(func_1)
    'func_1'

    >>> def parent_func(*args, **kwargs):
    ...     def nested_func():
    ...         pass
    ...     return nested_func
    ...
    >>> get_real_func_name(parent_func)
    'parent_func'

    >>> get_real_func_name(parent_func())
    'nested_func'

    >>> get_real_func_name(partial(parent_func, func_1))
    'parent_func'
    """

    fun_code = get_source_code(fun)
    tree = ast.parse(fun_code)
    parse_func = _ParseFuncName()
    try:
        parse_func.visit(tree)
    except _FuncParseFinished:
        pass

    return parse_func.name


class _FuncParseFinished(StopIteration):
    """_ParseFuncName finished parsing."""

class _ParseFuncName(ast.NodeVisitor):
    """
    A node visitor that stores a 'real' name of a parsed function to 'name' attribute
    and raises FuncNameParsed to stop .
    """
    def __init__(self):
        self.name = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.name = node.name
        raise _FuncParseFinished
