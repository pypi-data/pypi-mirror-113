import ast
import builtins
from typing import List, Set, Dict, Any

__all__ = ['CheckUsedGlobals']


class CheckUsedGlobals(ast.NodeVisitor):
    builtins = dir(builtins)

    def __init__(self):
        self.modules: Set[str] = set()
        self.imported: Set[str] = set()
        self.args: Set[str] = set()
        self.assigned_names: Set[str] = set()
        self.used_globals: Set[str] = set()

    def _check_assigned(self, name: str):
        return (
                name in self.assigned_names or
                name in self.builtins or
                name in self.args
        )

    def clear(self):
        self.modules.clear()
        self.imported.clear()
        self.args.clear()
        self.assigned_names.clear()
        self.used_globals.clear()

    def visit_Import(self, node: ast.Import):
        for import_name in node.names:
            self.modules.add(import_name.name.split('.')[0])
            self.imported.add(import_name.name)

            if import_name.asname:
                self.assigned_names.add(import_name.asname)
            else:
                name = import_name.name.split('.')[-1]
                self.assigned_names.add(name)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.modules.add(node.module.split('.')[0])

        for import_name in node.names:
            self.imported.add('.'.join([node.module, import_name.name]))
            if import_name.asname:
                self.assigned_names.add(import_name.asname)
            else:
                self.assigned_names.add(import_name.name)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        for name in self._get_names(node):
            self.update_globals(name)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> Any:
        self.assigned_names.update(list(self._get_names(node.target)))
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        for target_node in node.targets:
            self.assigned_names.update(list(self._get_names(target_node)))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.assigned_names.add(node.name)
        self.args.update(
            _get_funcdef_arg_names(node, 'posonlyargs') +
            _get_funcdef_arg_names(node, 'args') +
            _get_funcdef_arg_names(node, 'kwonlyargs')
        )
        if node.args.vararg:
            self.args.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.args.add(node.args.kwarg.arg)
        self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        self.used_globals.update(node.names)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        self.update_globals(node.id)
        self.generic_visit(node)

    def update_globals(self, name: str):
        if not self._check_assigned(name):
            self.used_globals.add(name)

    def _get_names(self, node):
        if isinstance(node, ast.Name):
            yield node.id
        elif isinstance(node, ast.Tuple):
            for n in node.elts:
                yield from self._get_names(n)
        elif isinstance(node, ast.Starred):
            yield from self._get_names(node.value)
        elif isinstance(node, ast.Call):
            yield from self._get_names(node.func)


def _get_funcdef_arg_names(node, attr) -> List[str]:
    arg_list = getattr(node.args, attr, None)
    if not arg_list:
        return []
    return list(map(lambda x: x.arg, getattr(node.args, attr)))
