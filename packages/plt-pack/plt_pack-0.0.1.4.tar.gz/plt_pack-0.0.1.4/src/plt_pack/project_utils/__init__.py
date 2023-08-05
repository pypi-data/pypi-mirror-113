from pathlib import Path
from datetime import datetime as dt
from functools import wraps
from typing import List


from ..file import save_plt_file, read_plt_file, PltFile


class PltProject(object):
    _TEST: bool = False

    def __init__(self, folder: Path or str, datefmt: str = '%d-%b-%H-%M-%S', format: str = 'plt'):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)
        self.datefmt = datefmt
        self.format = format

    def save(self, func,
             args: tuple = (),
             kwargs: dict = None,
             func_name: str = None,
             rewrite: bool = False) -> Path:
        func_name = func_name or func.__name__
        file_path = self.folder / _func_name(func_name, self.datefmt, rewrite, self.format)
        save_plt_file(file_path, func, *args, **(kwargs or {}))
        return file_path

    def auto_save(self, name: str = None, rewrite: bool = False):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self._TEST:
                    func(*args, **kwargs)
                self.save(func, args=args, kwargs=kwargs, func_name=name, rewrite=rewrite)

            return wrapper
        return decorator

    def list_files(self) -> List[str]:
        return [path.stem for path in self.folder.glob(f'*.{self.format}')]

    def load_file(self, name: str) -> PltFile:
        return read_plt_file(self.folder / f'{name}.{self.format}')

    def __getitem__(self, name: str):
        return self.load_file(name)

    @property
    def time_str(self):
        return time_str(self.datefmt)


def _func_name(func_name: str, datefmt: str, rewrite: bool, format: str = 'plt'):
    if rewrite:
        return f'{func_name}.{format}'
    else:
        return f'{func_name}-{time_str(datefmt)}.{format}'


def time_str(datefmt: str):
    return dt.now().strftime(datefmt)
