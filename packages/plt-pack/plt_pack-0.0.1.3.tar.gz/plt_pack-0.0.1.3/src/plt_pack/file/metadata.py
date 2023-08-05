import sys
from datetime import datetime as dt


def get_metadata() -> dict:
    platform = sys.platform
    py_version = sys.version
    time = dt.utcnow().strftime('%d %B %Y %H:%M:%S')
    return dict(time=time, py_version=py_version, platform=platform)


if __name__ == '__main__':
    print(get_metadata())
