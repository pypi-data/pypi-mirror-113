from types import FunctionType
from typing import Union, List, Dict, Any, Tuple, Optional
from io import BytesIO
from pathlib import Path

from ..jupyter_support import create_new_jupyter_cell, display_code

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
                     comments: bool = True,
                     ):
        code: List[str] = []

        entry_func_name = self.entry_func
        entry_func = self.functions[entry_func_name]
        sub_funcs = [
            self.functions[func_name]
            for func_name in sorted(self.functions.keys())
            if func_name != entry_func_name
        ]

        if with_imports:
            import_lines = '\n'.join(sorted(self.import_lines))
            if comments:
                import_lines = f'# Imports:\n{import_lines}'
            code.append(import_lines)

        if with_globals:
            global_lines = '\n'.join([f'{k} = {repr(v)}' for k, v in self.global_vars.items()])
            if comments:
                global_lines = f'# Global variables:\n{global_lines}'
            code.append(global_lines)

        if comments:
            code.append(f'# Main function:')

        code.append(entry_func)

        if with_subfunctions:
            if comments:
                code.append('# Sub-functions:')
            code += sub_funcs

        if exec_line:
            exec_str = f'\n\n{self.entry_func}(*PltFile_ARGS, **PltFile_KWARGS)'
            if comments:
                exec_str = f'# Execute function:\n{exec_str}'
            code.append(exec_str)

        return '\n\n'.join(code)

    def exec(self):
        code = self.get_code_str(exec_line=True, comments=False)

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
        display_code(self.get_code_str())


def save_plt_file(
        file: Union[str, Path, BytesIO],
        func: FunctionType,
        args: Optional[Tuple[Any, ...]] = (),
        kwargs: Optional[Dict[str, Any]] = None,
        info_dict: Optional[Dict[str, Any]] = None,
) -> PltFile:
    plt_file = PltFile.from_func(func, *args, **kwargs)
    if info_dict:
        plt_file.update(info_dict)
    plt_file.save(file)
    return plt_file


def read_plt_file(file: Union[str, Path, BytesIO]) -> PltFile:
    return PltFile(**read_file(file))
