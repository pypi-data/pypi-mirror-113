import ast
import builtins
from typing import List, Set, Dict

__all__ = ['CheckUsedGlobals']


class CheckUsedGlobals(ast.NodeVisitor):
    builtins = dir(builtins)

    def __init__(self):
        self.modules: Set[str] = set()
        self.imported: Set[str] = set()
        self.args: Set[str] = set()
        self.assigned_names: Set[str] = set()
        self.used_globals: Set[str] = set()

    def _check_assigned(self, name):
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

    def visit_Import(self, node):

        for import_name in node.names:
            self.modules.add(import_name.name.split('.')[0])
            self.imported.add(import_name.name)

            if import_name.asname:
                self.assigned_names.add(import_name.asname)
            else:
                name = import_name.name.split('.')[-1]
                self.assigned_names.add(name)

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.modules.add(node.module.split('.')[0])

        for import_name in node.names:
            self.imported.add('.'.join([node.module, import_name.name]))
            if import_name.asname:
                self.assigned_names.add(import_name.asname)
            else:
                self.assigned_names.add(import_name.name)

        self.generic_visit(node)

    def visit_Assign(self, node):
        assigned = list(map(lambda x: x.id, node.targets))
        self.assigned_names.update(assigned)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.assigned_names.add(node.name)
        self.args.update(
            _get_funcdef_arg_names(node, 'posonlyargs') +
            _get_funcdef_arg_names(node, 'args') +
            _get_funcdef_arg_names(node, 'kwonlyargs')
        )
        self.generic_visit(node)

    def visit_Global(self, node):
        self.used_globals.update(node.names)
        self.generic_visit(node)

    def visit_Name(self, node):
        if not self._check_assigned(node.id):
            self.used_globals.add(node.id)
        self.generic_visit(node)


def _get_funcdef_arg_names(node, attr) -> List[str]:
    return list(map(lambda x: x.arg, getattr(node.args, attr)))
