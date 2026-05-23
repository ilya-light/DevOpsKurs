import os

from pylint.checkers import BaseChecker


class ForbiddenNameChecker(BaseChecker):
    name = "forbidden-name-checker"
    priority = -1
    msgs = {
        "C9901": (
            "Variable name '%s' matches forbidden user name",
            "forbidden-user-variable",
            "Used when a variable name matches FORBIDDEN_VARIABLE_NAME.",
        ),
    }

    def open(self):
        raw_value = os.environ.get("FORBIDDEN_VARIABLE_NAME", "ivan")
        self.forbidden_names = {
            value.strip().lower()
            for value in raw_value.replace(";", ",").split(",")
            if value.strip()
        }

    def _check_name(self, node, variable_name):
        if variable_name.lower() in self.forbidden_names:
            self.add_message("forbidden-user-variable", node=node, args=(variable_name,))

    def visit_assignname(self, node):
        self._check_name(node, node.name)

    def visit_argname(self, node):
        self._check_name(node, node.name)


def register(linter):
    linter.register_checker(ForbiddenNameChecker(linter))
