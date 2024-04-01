from ..language_object import CoreObjectInterface, LanguageObjectInterface
from ..error import LineupError
from typing import Dict, Any, List


class VariableNotExistError(LineupError):
    pass


class DeleteDefaultVariableError(LineupError):
    pass


class VariableObject(CoreObjectInterface):
    variables: Dict[str, Any]
    default_variables: List[str]

    def __init__(self, variables: Dict[str, Any] = {}) -> None:
        self.variables = variables
        self.default_variables = list(variables.keys())
        self.functions = {
            "VAR": self._variable,
        }

    def close(self):
        for key in self.variables.keys():
            if type(self.variables[key]) is LanguageObjectInterface:
                self.variables[key].close()

    def reset(self):
        variables_delete = [key for key in self.variables.keys()
                            if key not in self.default_variables]
        for key in variables_delete:
            if type(self.variables[key]) is LanguageObjectInterface:
                self.variables[key].reset()
            del self.variables[key]
        for key in self.variables.keys():
            if type(self.variables[key]) is LanguageObjectInterface:
                self.variables[key].reset()

    def _get(self, name: str):
        if name in self.variables:
            return self.variables[name]
        raise VariableNotExistError(f"'{name}' not exist in '{self}'")

    def _set(self, name: str, value):
        self.variables[name] = value

    def _delete(self, name: str):
        if name in self.default_variables:
            raise DeleteDefaultVariableError(
                f"'{name}' is default variable in '{self}'")
        if name in self.variables:
            del self.variables[name]

    def _execute_in_variables(self, variables, function_name: str, *args):
        if variables in self.variables:
            return self.variables[variables].execute(function_name, *args)
        return None

    def _execute_from_executor(self, line: List[str]):
        return self.executor.execute_line(line)

    def _variable(self, name: str, command: str, *args):
        if command == "USE":
            self._set(name, self._execute_in_variables(args[0], args[1], *args[2:]))
        elif command == "COPY":
            self._set(name, self._get(args[0]))
        elif command == "UNSET":
            self._delete(name)
        elif command == "GET":
            return self._get(name)
        elif command == "SET":
            self._set(name, args[0])
        elif command == "EXEC":
            return self._set(name, self._execute_from_executor(args))
        return None
