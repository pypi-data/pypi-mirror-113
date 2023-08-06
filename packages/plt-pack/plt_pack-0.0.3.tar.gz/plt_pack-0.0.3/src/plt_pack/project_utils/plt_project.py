import logging
from pathlib import Path
from datetime import datetime as dt
from functools import wraps
from typing import List, Dict, Tuple, Any, Optional, Union
from types import FunctionType
from contextlib import contextmanager

import matplotlib.pyplot as plt

from .save_opts import SaveOpts, PLT_FORMAT, add_opt_docs
from ..file import save_plt_file, read_plt_file, PltFile


@add_opt_docs
class PltProject(object):

    """
    Args:
        folder (Path/str): A base folder of a new project. All the files will be saved to this folder.
        save_opts (SaveOpts, optional): Default save options. Can be provided as an object or using the keyword 
            arguments from below. 
        {save_opt_args}
    """

    _TEST: bool = False

    def __init__(self,
                 folder: Path or str,
                 save_opts: Optional[SaveOpts] = None,
                 **save_opt_kwargs,
                 ):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)

        self.default_opts: SaveOpts = save_opts or SaveOpts(**save_opt_kwargs)
        self._context_opts: SaveOpts = SaveOpts()

    @property
    def context_opts(self) -> Optional[SaveOpts]:
        return self._context_opts

    @add_opt_docs
    def get_save_opts(self, **kwargs) -> SaveOpts:
        """
        Args:
            {save_opt_args}
        """
        return self.context_opts.\
            new_opts(only_missing_keys=True, **kwargs).\
            new_opts(only_missing_keys=True, **self.default_opts)

    @contextmanager
    @add_opt_docs
    def __call__(self,
                 save_opts: SaveOpts = None,
                 **save_opt_kwargs
                 ):
        """
        Args:
            folder (Path/str): A base folder of a new project. All the files will be saved to this folder.
            save_opts (SaveOpts, optional): Default save options. Can be provided as an object or using the keyword 
                arguments from below. 
        {save_opt_args}
        """

        self._context_opts = save_opts or SaveOpts(**save_opt_kwargs)
        try:
            yield
        finally:
            self._context_opts = SaveOpts()

    @add_opt_docs
    def save(self,
             func: FunctionType,
             args: Optional[Tuple[Any, ...]] = (),
             kwargs: Optional[Dict[str, Any]] = None,
             save_opts: Optional[SaveOpts] = None,
             **save_opt_kwargs,
             ) -> Path:

        """
        Save a function and its arguments based on provided save options.
        
        Args:
            func (FunctionType): Function to save.
            args (tuple, optional): Positional arguments.
            kwargs (dict, optional): Keyword arguments.
            save_opts (SaveOpts, optional): Current save options. Can be provided as an object or 
                using the keyword arguments from below.
            {save_opt_args}
        """
        save_opts = self.get_save_opts(**(save_opts or save_opt_kwargs))
        plt_name, fig_name = save_opts.get_names(func)
        plt_path = self.folder / plt_name

        kwargs = kwargs or {}

        if save_opts.save_figure:
            _save_figure(func, self.folder / fig_name, args, kwargs)

        if save_opts.save_plt:
            save_plt_file(plt_path, func, *args, **kwargs)

        return plt_path

    def register(self, func: FunctionType):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self._register_called(func, args, kwargs)

        return wrapper

    @add_opt_docs
    def auto_save(self, save_opts: Optional[SaveOpts] = None, **save_opt_kwargs):
        """
        A decorator that registers a decorated function with
        Args:
            save_opts:
            {save_opt_args}

        Returns:

        """
        default_save_opts: SaveOpts = save_opts or SaveOpts(**save_opt_kwargs)

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self._TEST:
                    func(*args, **kwargs)
                self.save(func, args, kwargs, **default_save_opts)

            return wrapper

        return decorator

    def list_files(self) -> List[str]:
        return [path.stem for path in self.folder.glob(f'*.{PLT_FORMAT}')]

    def load_file(self, name: str) -> PltFile:
        return read_plt_file(self.folder / f'{name}.{PLT_FORMAT}')

    def __getitem__(self, name: str):
        return self.load_file(name)

    def _register_called(self, func: FunctionType, args: List[Any], kwargs: Dict[str, Any]):
        if not self._TEST:
            func(*args, **kwargs)
        if self._context_opts:
            self.save(func, args, kwargs)


def _save_figure(
        func: FunctionType,
        path: Path,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any]
):

    path = str(path.absolute())
    plt.ioff()
    try:
        func(*args, **kwargs)
    except Exception as err:
        logger = logging.getLogger(__name__)
        logger.exception(err)
        logger.error(f'Function execution failed. Could not save to {path}.')
    plt.savefig(path)
    plt.ion()
