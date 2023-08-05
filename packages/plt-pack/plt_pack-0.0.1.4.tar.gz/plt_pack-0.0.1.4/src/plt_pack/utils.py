from .msgpack_import import msgpack


__all__ = ['find_non_serializable', 'is_serializable']


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
