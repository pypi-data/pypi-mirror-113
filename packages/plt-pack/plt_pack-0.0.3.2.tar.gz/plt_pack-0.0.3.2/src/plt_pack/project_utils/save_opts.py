from types import FunctionType
from typing import Tuple, Dict, Any, Optional
import datetime

from ..parse.parse_func_name import get_real_func_name
from ..utils import format_docs

__all__ = ['SaveOpts', 'add_opt_docs']

PLT_FORMAT: str = 'plt'

SAVE_OPTS_DOCSTRING: str = f"""
    name (str, optional): Name of the function. If not provided, __name__ attribute is used.
    rewrite (bool, optional): Rewrite the .{PLT_FORMAT} file. False by default.
    datefmt (str, optional): Date format for file name. Default format is '%d-%b-%H-%M-%S'.
        While providing a custom format, check the requirements of the OS regarding the allowed 
        charachters for file names.
    suffix (str, optional): Adds an suffix to the file name.
    save_figure (bool, optional): (experimental feature) Execute function and save the figure along 
        with the .{PLT_FORMAT} file. It is assumed that a function creates a figure via matplotlib package.
         False by default.
    fig_format (str, optional): (experimental feature) Figure format used if save_figure is True.
        Default format is 'eps'.
    save_plt (bool, optional): Save .{PLT_FORMAT} file. True by default. 
    description (str, optional): Description of the function to be saved in a .{PLT_FORMAT} file.
"""

add_opt_docs = format_docs(SAVE_OPTS_DOCSTRING, 'save_opt_args')


# dataclasses are not available in python 3.6 =/
class SaveOpts(dict):
    """
    Args:
        {save_opt_args}

    """

    _DEFAULTS = {
        'name': None,
        'rewrite': False,
        'suffix': None,
        'datefmt': '%d-%b-%H-%M-%S',
        'save_figure': False,
        'fig_format': 'eps',
        'save_plt': True,
        'description': None,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def info_dict(self) -> Dict[str, Any]:
        return {'description': self.description or ''}

    def new_opts(self, only_missing_keys: bool = False, **kwargs) -> 'SaveOpts':
        if only_missing_keys:
            base_kwargs, add_kwargs = kwargs, self
        else:
            base_kwargs, add_kwargs = self, kwargs

        opts_dict = SaveOpts(**base_kwargs)
        opts_dict.update(**add_kwargs)
        return opts_dict

    def __repr__(self):
        args = ', '.join([f'{k}={repr(v)}' for k, v in self.items()])
        return f'SaveOpts({args})'

    @property
    def time_str(self) -> str:
        return datetime.datetime.now().strftime(self.datefmt)

    def get_names(self, func: FunctionType = None) -> Tuple[str, str]:
        func_name = self._get_func_name(func)

        return self._get_file_names_from_func_name(func_name)

    def _fget(self, name: str):
        return self.get(name, self._DEFAULTS[name])

    @property
    def name(self):
        return self._fget('name')

    @property
    def rewrite(self):
        return self._fget('rewrite')

    @property
    def suffix(self):
        return self._fget('suffix')

    @property
    def datefmt(self):
        return self._fget('datefmt')

    @property
    def save_figure(self):
        return self._fget('save_figure')

    @property
    def fig_format(self):
        return self._fget('fig_format')

    @property
    def save_plt(self):
        return self._fget('save_plt')

    @property
    def description(self):
        return self._fget('description')

    def _get_func_name(self, func: FunctionType = None) -> str:
        func_name = self.name or _get_func_name(func)

        if self.suffix:
            func_name = f'{func_name}_{self.suffix}'

        if not self.rewrite:
            func_name = f'{func_name}_{self.time_str}'

        return func_name

    def _get_file_names_from_func_name(self, func_name: str) -> Tuple[str, str]:
        return f'{func_name}.{PLT_FORMAT}', f'{func_name}.{self.fig_format}'


def _get_func_name(func: FunctionType) -> str:
    try:
        return func.__name__
    except AttributeError:
        return get_real_func_name(func)
