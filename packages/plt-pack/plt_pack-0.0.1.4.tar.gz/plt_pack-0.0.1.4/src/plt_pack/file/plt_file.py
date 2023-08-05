from types import FunctionType
from typing import Union, List
from io import BytesIO
from pathlib import Path

from ..jupyter_support import create_new_jupyter_cell, jupyter_code

from ..parse import FuncDict
from .save_read import save_file, read_file
from .file_dict import get_file_dict

__all__ = ['PltFile', 'save_plt_file', 'read_plt_file']


class PltFile(FuncDict):
    def get_code_str(self,
                     with_imports: bool = True,
                     with_subfunctions: bool = True,
                     with_globals: bool = True,
                     exec_line: bool = False,
                     ):
        code: List[str] = []

        entry_func_name = self.entry_func
        entry_func = self.functions[entry_func_name]
        sub_funcs = [func for func_name, func in self.functions.items()
                     if func_name != entry_func_name]

        if with_imports:
            import_lines = '\n'.join(self.import_lines)
            code.append(import_lines)

        if with_globals:
            global_lines = '\n'.join([f'{k} = {v}' for k, v in self.global_vars.items()])
            code.append(global_lines)

        code.append(entry_func)

        if with_subfunctions:
            code += sub_funcs

        if exec_line:
            exec_str = f'\n\n{self.entry_func}(*PltFile_ARGS, **PltFile_KWARGS)'
            code.append(exec_str)

        return '\n\n'.join(code)

    def exec(self):
        code = self.get_code_str(exec_line=True)

        global_dict = {
            'PltFile_ARGS': self.args,
            'PltFile_KWARGS': self.kwargs,
        }
        exec(code, global_dict)

    @classmethod
    def from_func(cls, func: FunctionType, *args, **kwargs):
        func_dict = get_file_dict(func, *args, **kwargs)
        return cls(**func_dict)

    @classmethod
    def from_file(cls, file: Union[str, Path, BytesIO]):
        return cls(**read_file(file))

    def save(self, file: Union[str, Path, BytesIO]):
        save_file(file, self)

    def show_code(self, with_imports: bool = True, with_subfunctions: bool = True, with_globals: bool = True):
        code = self.get_code_str(with_imports, with_subfunctions, with_globals)
        try:
            create_new_jupyter_cell(code)
        except ImportError:
            return code

    def _ipython_display_(self):
        return jupyter_code(self.get_code_str())


def save_plt_file(file: Union[str, Path, BytesIO], func: FunctionType, *args, **kwargs) -> PltFile:
    plt_file = PltFile.from_func(func, *args, **kwargs)
    plt_file.save(file)
    return plt_file


def read_plt_file(file: Union[str, Path, BytesIO]) -> PltFile:
    return PltFile(**read_file(file))
