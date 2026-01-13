from __future__ import annotations

import argparse
import ast
from collections.abc import Sequence


class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls: set[str] = set()

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        self.generic_visit(node)


def check_file(content: bytes, filename: str) -> bool:
    tree = ast.parse(content)
    functions: list[tuple[str, int, set[str]]] = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            visitor = FunctionCallVisitor()
            visitor.visit(node)
            functions.append((node.name, node.lineno, visitor.calls))

    valid = True
    defined_order = {name: i for i, (name, _, _) in enumerate(functions)}

    for i, (name, lineno, calls) in enumerate(functions):
        for call in calls:
            if call in defined_order and defined_order[call] < i:
                print(f"{filename}:{lineno}: Function '{name}' calls '{call}' defined earlier.")
                valid = False

    return valid


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, 'rb') as f:
                if not check_file(f.read(), filename=filename):
                    retval = 1
        except Exception as e:
            print(f'Error: {e}')
            retval = 1
    return retval


if __name__ == '__main__':
    raise SystemExit(main())
