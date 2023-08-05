from types import FunctionType

from ..parse import parse_function
from ..__version import __version__

from .misc import get_diff_rc_params
from .metadata import get_metadata


def get_file_dict(func: FunctionType, *args, **kwargs) -> dict:
    func_dict: dict = parse_function(func)
    diff_rc = get_diff_rc_params()
    metadata = get_metadata()
    func_dict.update({
        'args': args,
        'kwargs': kwargs,
        '__version__': __version__,
        'metadata': metadata,
        'diff_rc': diff_rc,
    })
    return func_dict
