from typing import Union

from pathlib import Path
from io import BytesIO

from .misc import _open_file_from_args, CorruptedPltFileError, NonSerializableDataError

from ..msgpack_import import msgpack
from ..utils import is_serializable, find_non_serializable


def read_file(file: Union[str, Path, BytesIO]) -> dict:
    with _open_file_from_args(file, 'rb') as f:
        try:
            return msgpack.unpack(f)
        except Exception as err:
            raise CorruptedPltFileError from err


def save_file(file: Union[str, Path, BytesIO], file_dict: dict):
    with _open_file_from_args(file, 'wb') as f:
        try:
            msgpack.pack(file_dict, f)
        except TypeError as err:
            keys = find_non_serializable(file_dict)

            internal_err_keys = []
            err_msg = f''
            raise NonSerializableDataError from err
