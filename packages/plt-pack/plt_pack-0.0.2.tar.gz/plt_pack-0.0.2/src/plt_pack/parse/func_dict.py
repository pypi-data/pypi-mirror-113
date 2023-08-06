from typing import Dict, Tuple, Any

__all__ = ['FuncDict']


class FuncDict(dict):
    def __init__(self,
                 entry_func: str,
                 functions: Dict[str, str],
                 modules: Tuple[str, ...],
                 import_lines: Tuple[str, ...],
                 module_versions: Dict[str, str],
                 global_vars: Dict[str, Any],
                 **kwargs
                 ):
        super().__init__()
        self.update(dict(
            entry_func=entry_func,
            functions=functions,
            modules=modules,
            import_lines=import_lines,
            module_versions=module_versions,
            global_vars=global_vars,
        ))
        self.update(kwargs)

    # Mandatory keys
    @property
    def entry_func(self) -> str:
        return self['entry_func']

    @property
    def functions(self) -> Dict[str, str]:
        return self['functions']

    @property
    def modules(self) -> Tuple[str, ...]:
        return self['modules']

    @property
    def import_lines(self) -> Tuple[str, ...]:
        return self['import_lines']

    @property
    def module_versions(self) -> Dict[str, str]:
        return self['module_versions']

    @property
    def global_vars(self) -> Dict[str, Any]:
        return self['global_vars']

    # Optional keys

    @property
    def args(self) -> Tuple[Any, ...]:
        return self.get('args', ())

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self.get('kwargs', {})

    @property
    def version(self) -> str:
        return self.get('__version__', '')

    @property
    def metadata(self) -> str:
        return self.get('metadata', '')

    @property
    def diff_rc(self) -> Dict[str, Any]:
        return self.get('diff_rc', {})
