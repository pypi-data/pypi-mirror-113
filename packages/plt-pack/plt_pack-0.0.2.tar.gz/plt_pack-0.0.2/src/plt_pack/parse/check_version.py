import importlib
from types import ModuleType

__all__ = ['check_version']

try:
    from importlib.metadata import version  # python 3.8 or above


    def check_version(module: str or ModuleType) -> str or None:
        if isinstance(module, ModuleType):
            if module.__package__:
                try:
                    return version(module.__package__)
                except ImportError:
                    return check_version(module.__name__)
        else:
            try:
                return version(module)
            except ImportError:
                try:
                    return version(module.split('.')[0])
                except ImportError:
                    return


except ImportError:

    from packaging.version import parse as parse_version
    from packaging.version import Version


    def check_version(module: str or ModuleType) -> str or None:
        if isinstance(module, str):
            module = _str_to_module(module)

            if not module:
                return

        if hasattr(module, '__version__'):
            version = module.__version__
            if _version_is_valid(version):
                return version
        if (
                hasattr(module, '__package__') and
                module.__package__ and
                module.__name__ != module.__package__
        ):
            return check_version(module.__package__)


    def _version_is_valid(version_str: str) -> bool:
        return isinstance(parse_version(version_str), Version)


    def _str_to_module(module: str) -> ModuleType or None:
        try:
            module = globals()[module]
        except KeyError:
            try:
                return importlib.import_module(module)
            except ImportError:
                return
