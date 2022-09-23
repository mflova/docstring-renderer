import ast
from typing import List, Sequence, final


class AstRunnerError(Exception):
    """Exceptions raised by `AstRunner` objects."""


@final
class AstRunner:
    def __init__(self, file_path: str, keyword: str) -> None:
        with open(file_path) as file:
            self.node = ast.parse(file.read())
        self.keyword = keyword

    def list_funcs(self) -> Sequence[str]:
        functions = [n for n in self.node.body if isinstance(n, ast.FunctionDef)]
        res = []
        for function in functions:
            res.append(function.name)
        return res

    def list_methods(self) -> Sequence[str]:
        classes = [n for n in self.node.body if isinstance(n, ast.ClassDef)]
        res = []
        for class_ in classes:
            methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
            for method in methods:
                res.append(f"{class_.name}.{method.name}")
        return res

    def list_classes(self) -> Sequence[str]:
        classes = [n for n in self.node.body if isinstance(n, ast.ClassDef)]
        res: List[str] = []
        for class_ in classes:
            res.append(class_.name)
        return res

    def list_all(self) -> Sequence[str]:
        names: List[str] = []
        names.extend(self.list_funcs())
        names.extend(self.list_methods())
        names.extend(self.list_classes())
        return names

    def find_keyword(self) -> str:
        shortest_match = ""
        for elem in self.list_all():
            if self.keyword in elem and -len(elem) < len(shortest_match):
                shortest_match = elem

        if not shortest_match:
            raise AstRunnerError(
                "Among all defined methods/funcs/classes, no objects could be found "
                f"with the keyword `{self.keyword}` in the name."
            )
        return shortest_match
