import ast
from inspect import getsource
import logging
import importlib

from types import (
    FunctionType,
    ModuleType,
)

from typing import (
    NamedTuple,
    Dict,
    Any,
    List,
    Tuple,
)

from .func_dict import FuncDict
from .check_used_globals import CheckUsedGlobals
from .check_version import check_version
from ..utils import is_serializable, find_non_serializable

__all__ = ['FuncParser', 'parse_function']



def parse_function(fun: FunctionType) -> FuncDict:
    return FuncParser().parse_func(fun)


class FuncParser(object):
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.check_globals = CheckUsedGlobals()
        self.used_modules = set()
        self.import_lines = set()
        self.global_vars = {}
        self._unparsed_functions = {}
        self.parsed_functions = {}
        self.module_versions = {}
        self.func_dict = {}
        self.src_module: str = None
        self.entry_func: str = None

    def clear(self):
        self.used_modules.clear()
        self.import_lines.clear()
        self.global_vars.clear()
        self._unparsed_functions.clear()
        self.parsed_functions.clear()
        self.module_versions.clear()
        self.func_dict.clear()
        self.src_module = None
        self.entry_func = None

    def parse_func(self, fun: FunctionType) -> FuncDict:
        if not isinstance(fun, FunctionType):
            raise TypeError(f'Only FunctionType objects supported, got {type(fun).__name__}.')

        self.clear()

        self.entry_func = fun.__name__

        self.src_module = fun.__module__ if hasattr(fun, '__module__') else '__main__'

        self._parse_func(fun)
        self._update_module_versions(fun)
        return self.to_func_dict()

    def _parse_func(self, fun: FunctionType):
        if fun.__name__ in self.parsed_functions:
            return

        self.check_globals.clear()
        fun_code = getsource(fun)
        fun_code = _fix_func_code(fun_code)
        tree = ast.parse(fun_code)
        self.check_globals.visit(tree)

        self.used_modules.update(self.check_globals.modules)
        self._parse_globals(fun)
        self.parsed_functions[fun.__name__] = fun_code

        unparsed_functions = dict(self._unparsed_functions)
        self._unparsed_functions.clear()

        for fun in unparsed_functions.values():
            self._parse_func(fun)

    def _update_module_versions(self, fun: FunctionType):
        for module_name in self.used_modules:
            try:
                module = importlib.import_module(module_name)
                version = check_version(module)
            except (TypeError, ImportError):
                continue
            if version:
                self.module_versions[module_name] = version
            else:
                self.log.warning(f'Could not retrieve the version of the module {module_name}.')

    def _parse_globals(self, fun: FunctionType):
        for name in self.check_globals.used_globals:
            self._parse_global_name(fun, name)

    def _parse_global_name(self, fun, name) -> None:
        var, status = _get_global_var_from_name(name, fun)

        if not status:
            self.log.warning(f'Could not find a global variable {name}.')
            return

        if self._is_duplicate(var, name):
            return

        if self._parse_module_type(var, name):
            return

        if self._parse_imported_object(var, name):
            return

        if isinstance(var, FunctionType):
            self._unparsed_functions[name] = var
        elif is_serializable(var):
            self.global_vars[name] = var
        else:
            raise TypeError(f'Global var {name} is not serializable: {find_non_serializable(var)}.')

    def _parse_imported_object(self, var, name) -> bool:
        if hasattr(var, '__module__'):
            module_name = var.__module__
            if module_name != self.src_module:
                var_name = var.__name__ if hasattr(var, '__name__') else name
                self.import_lines.add(_get_import_line(var_name, module_name, name))
                self.used_modules.add(module_name.split('.')[0])
                return True
        return False

    def _is_duplicate(self, var, name) -> bool:
        if name in self._unparsed_functions and self._unparsed_functions[name] == var:
            return True
        if name in self.global_vars and self.global_vars[name] == var:
            return True
        return False

    def _parse_module_type(self, var: ModuleType, assigned_name) -> bool:
        if not isinstance(var, ModuleType):
            return False
        try:
            module_name = var.__name__
        except AttributeError:
            self.log.warning(f'Failed getting a module name: {var}, use {assigned_name} instead.')
            module_name, assigned_name = assigned_name, None
        self.import_lines.add(_get_import_line(module_name, assigned_name=assigned_name))
        self.used_modules.add(module_name.split('.')[0])
        return True

    def to_func_dict(self) -> FuncDict:
        return FuncDict(
            entry_func=self.entry_func,
            functions=dict(self.parsed_functions),
            modules=tuple(self.used_modules),
            import_lines=tuple(self.import_lines),
            module_versions=dict(self.module_versions),
            global_vars=dict(self.global_vars),
        )


def _get_global_var_from_name(name, fun) -> Tuple[Any, bool]:
    try:
        var = fun.__globals__[name]
    except KeyError:
        if name in globals():
            var = globals()[name]
        else:
            return None, False
    return var, True


def _get_import_line(name: str, from_str: str = None, assigned_name: str = None) -> str:
    if from_str:
        line = f'from {from_str} import {name}'
    else:
        line = f'import {name}'
    if assigned_name and assigned_name != name:
        line = f'{line} as {assigned_name}'
    return line


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
