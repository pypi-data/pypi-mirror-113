from typing import Union
from io import BytesIO
from contextlib import contextmanager
from pathlib import Path

import matplotlib.pyplot as plt


def get_diff_rc_params():
    return {
        k: v for k, v in plt.rcParams.items()
        if (
                v != plt.rcParamsDefault[k] and
                k != 'axes.prop_cycle'
        )
    }


class NotAPltFileError(TypeError):
    pass


class CorruptedPltFileError(IOError):
    pass


class NonSerializableDataError(TypeError):
    pass


@contextmanager
def _open_file_from_args(file: Union[str, Path, BytesIO], mode: str = 'rb', *args, **kwargs):
    if isinstance(file, Path):
        file = str(file.absolute())

    if isinstance(file, str):
        with open(file, mode, *args, **kwargs) as f:
            yield f
        return
    elif hasattr(file, 'read'):
        yield file  # we do not close it since we did not open it ourselves
        return
    raise TypeError(f'Expected a file or a path-like object, received {file} instead.')
