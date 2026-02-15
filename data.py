import ast
import os
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional, TypeAlias

from git import Repo


@dataclass
class FunctionItem:
    type: Literal["function", "method"]
    name: str
    class_name: str
    start_line: int
    end_line: int
    code: str
    docstring: str
    params: str
    file_path: Optional[str] = None


@dataclass
class ClassItem:
    type: Literal['class']
    name: str
    start_line: int
    end_line: int
    code: str
    docstring: str
    bases: str
    file_path: Optional[str] = None


Item: TypeAlias = FunctionItem | ClassItem
Embeddings: TypeAlias = List[float]


class CodeChunkVisitor(ast.NodeVisitor):
    def __init__(self, source: str):
        self.chunks = []
        self.current_class = None
        self._source = source

    def visit_FunctionDef(self, node):
        chunk = extract_function_chunk(node, self._source, self.current_class)
        self.chunks.append(chunk)

    def visit_ClassDef(self, node):
        self.current_class = node.name
        class_chunk = extract_class_chunk(node, self._source)
        self.chunks.append(class_chunk)

        self.generic_visit(node)
        self.current_class = None  # Reset after class

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)


def _split_code_by_ast(file_path: str) -> List[Item]:
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)

    visitor = CodeChunkVisitor(source)
    visitor.visit(tree)

    return visitor.chunks


def extract_function_chunk(node: ast.FunctionDef, source: str, class_name: str = None) -> FunctionItem:
    start_line = node.lineno - 1
    end_line = node.end_lineno - 1 if hasattr(node, 'end_lineno') else start_line + 20

    func_lines = source.splitlines(keepends=True)[start_line:end_line + 1]
    func_code = ''.join(func_lines)

    func_code = textwrap.dedent(func_code)

    function_item = FunctionItem(
        type="function" if class_name is None else "method",
        name=f'{class_name}.{node.name}',
        class_name=class_name,
        start_line=node.lineno,
        end_line=end_line + 1,
        code=func_code.strip(),
        docstring=ast.get_docstring(node) or "",
        params=', '.join([str(arg.arg) for arg in node.args.args if hasattr(arg, 'arg')])
    )

    return function_item


def extract_class_chunk(node: ast.ClassDef, source: str) -> ClassItem:
    start_line = node.lineno - 1
    end_line = node.end_lineno - 1

    class_code = '\n'.join(source.splitlines(keepends=True)[start_line:end_line])

    items = ClassItem(
        type="class",
        name=node.name,
        start_line=node.lineno,
        end_line=node.end_lineno,
        code=class_code.strip(),
        docstring=ast.get_docstring(node) or "",
        bases=', '.join([base.id for base in node.bases if isinstance(base, ast.Name)])
    )

    return items


def clone_repo(repo_url: str, local_path):
    if not os.path.exists(local_path):
        Repo.clone_from(repo_url, local_path)
        print(f"Cloned {repo_url} to {local_path}")
    else:
        print("Repo already exists")


def split_code_from_repo_into_items(repo_path: str, target_dirs: List[str]) -> List[Item]:
    all_items = []
    for folder in target_dirs:
        folder_path = Path(repo_path) / folder
        for file_path in folder_path.rglob('*.py'):
            print(f"Processing {file_path}")

            items = _split_code_by_ast(str(file_path))
            for item in items:
                item.file_path = str(file_path.relative_to(repo_path))
                all_items.append(item)

    return all_items
