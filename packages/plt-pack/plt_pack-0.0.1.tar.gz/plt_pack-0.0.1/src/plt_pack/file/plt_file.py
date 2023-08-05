from types import FunctionType
from typing import Union
from io import BytesIO
from pathlib import Path

from ..jupyter_support import create_new_jupyter_cell, jupyter_code

from .save_read import save_file, read_file
from .file_dict import get_file_dict

__all__ = ['PltFile', 'save_plt_file', 'read_plt_file']


class PltFile(object):
    def __init__(self, func: FunctionType = None, *args, _file_dict: dict = None, **kwargs):
        if _file_dict:
            self.file_dict = _file_dict
        else:
            self.file_dict = get_file_dict(func, *args, **kwargs)

    def get_code_str(self, with_imports: bool = True, with_subfunctions: bool = True, with_globals: bool = True):
        code = ''

        entry_func_name = self.file_dict['entry_func']
        entry_func = self.file_dict['functions'][entry_func_name]
        sub_funcs = [func for func_name, func in self.file_dict['functions'].items()
                     if func_name != entry_func_name]

        if with_imports:
            import_lines = '\n'.join(self.file_dict['import_lines'])
            code += import_lines
            code += '\n\n'

        if with_globals:
            global_lines = '\n'.join([f'{k} = {v}' for k, v in self.file_dict['global_vars'].items()])
            code += global_lines
            code += '\n\n'

        code += entry_func

        if with_subfunctions:
            code += '\n\n'
            code += '\n\n'.join(sub_funcs)

        return code

    @property
    def used_modules(self):
        return self.file_dict['modules']

    @classmethod
    def from_file(cls, file: Union[str, Path, BytesIO]):
        return cls(_file_dict=read_file(file))

    def save(self, file: Union[str, Path, BytesIO]):
        save_file(file, self.file_dict)

    def show_code(self, with_imports: bool = True, with_subfunctions: bool = True, with_globals: bool = True):
        code = self.get_code_str(with_imports, with_subfunctions, with_globals)
        try:
            create_new_jupyter_cell(code)
        except ImportError:
            return code

    def _ipython_display_(self):
        return jupyter_code(self.get_code_str())


def save_plt_file(file: Union[str, Path, BytesIO], func: FunctionType, *args, **kwargs) -> PltFile:
    plt_file = PltFile(func, *args, **kwargs)
    plt_file.save(file)
    return plt_file


def read_plt_file(file: Union[str, Path, BytesIO]) -> PltFile:
    return PltFile(_file_dict=read_file(file))
