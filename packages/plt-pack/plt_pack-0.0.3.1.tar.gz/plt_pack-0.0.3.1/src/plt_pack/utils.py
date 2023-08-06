import unicodedata
import re
from typing import Optional, Any
from types import FunctionType

from .msgpack_import import msgpack


__all__ = ['find_non_serializable', 'is_serializable', 'str2valid_filename']


def format_docs(docs: str, docs_name: Optional[str] = None) -> object:
    """
    Returns a decorator that modifies an object docstring by either inserting docs instead of '{[docs_name]}'
    ([docs_name] stands for docs_name keyword here) or by replacing docstring by docs if docs_name
    is not provided.

    Args:
        docs (str): Docstring to be inserted (or replaced) into the decorated object docstring.
        docs_name (str, optional): Format keyword.

    Returns:
        FunctionType: A decorator that modifies object docstring and returns the object.

    Examples:
        >>> @format_docs('Some docstring.')
        ... def func1():
        ...     pass
        ...
        >>> func1.__doc__
        'Some docstring.'

        >>> @format_docs('arguments', 'docs')
        ... def func2():
        ...     '''Docstring with {docs}.'''
        ...     pass
        ...
        >>> func2.__doc__
        'Docstring with arguments.'

        >>> @format_docs('arguments', 'docs')
        ... def func2():
        ...     '''Docstring with {docs}.'''
        ...     pass
        ...
        >>> func2.__doc__
        'Docstring with arguments.'

        >>> docs = '''
        ... argument1
        ... argument2'''

        >>> @format_docs(docs, 'docs')
        ... def func3():
        ...     '''Multiline docstring.
        ...         {docs}
        ... '''
        ...     pass
        ...
        >>> print(func3.__doc__)
        Multiline docstring.
        <BLANKLINE>
                argument1
                argument2
        <BLANKLINE>
        >>> @format_docs(docs, 'docs')
        ... def func4():
        ...     '''
        ...     Multiline docstring.
        ...         {docs}
        ... '''
        ...     pass
        ...
        >>> print(func4.__doc__)
        <BLANKLINE>
            Multiline docstring.
        <BLANKLINE>
            argument1
            argument2
        <BLANKLINE>
    """

    def decorator(obj: object) -> object:
        if docs_name:
            obj.__doc__ = _modify_docstring(obj.__doc__, docs, docs_name)
            return obj
        else:
            obj.__doc__ = docs
        return obj

    return decorator


def _modify_docstring(src_doc: str, new_doc: str, docs_name: str) -> str:
    key = '{%s}' % docs_name
    doc_lines = src_doc.split('\n')
    first_doc_line = ''

    for num, line in enumerate(doc_lines):
        if not first_doc_line and line:
            first_doc_line = line
        if key in line:
            break
    else:  # no docs_name found
        return src_doc

    init_indentation: int = _get_indentation(first_doc_line)

    target_indentation: int = _get_indentation(line.split(key)[0]) - init_indentation

    indentation = ' ' * target_indentation

    formatted_docs = f'\n{indentation}'.join(new_doc.split('\n'))

    doc_lines[num] = line.replace(key, formatted_docs)

    return '\n'.join(doc_lines)


def _get_indentation(src: str) -> int:
    src = src.replace('\t', ' ' * 4)
    return len(src) - len(src.lstrip(' '))


def str2valid_filename(value: str) -> str:
    """
    Adapted from https://github.com/django/django/blob/master/django/utils/text.py
    Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.

    Args:
        value (str): Initial name of a file.
    Returns:
        str: A valid file name.

    Examples:
        >>> str2valid_filename('2 Jun 02:15:45')
        '2-jun-02-15-45'

        >>> str2valid_filename('path/to\dir')
        'path-to-dir'
    """
    value = unicodedata.normalize('NFKC', value)
    value = re.sub(r'[^\w\s-]', ' ', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def is_serializable(data) -> bool:
    try:
        msgpack.packb(data)
        return True
    except TypeError:
        return False


def find_non_serializable(data: dict or list):
    return _find_non_serializable(data)


def _find_non_serializable(data: dict or list, *, prev_keys=None) -> list:
    _found_keys = []

    prev_keys = prev_keys or []

    if isinstance(data, (list, tuple)):
        data = {str(i): v for i, v in enumerate(data)}

    for key, value in data.items():
        if isinstance(value, (list, tuple, dict)):
            _found_keys += _find_non_serializable(value, prev_keys=prev_keys + [key])
        else:
            if not is_serializable(value):
                _found_keys.append(prev_keys + [key])
    return _found_keys
