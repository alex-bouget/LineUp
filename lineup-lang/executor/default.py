from ..language_object import LanguageExecutorInterface, \
    CoreObjectInterface
from ..error import ExecutorFunctionAlreadyExistError, \
    ExecutorFunctionNotExistError
from typing import Any, List


class DefaultExecutor(LanguageExecutorInterface):
    stop = False

    def __init__(self, core_object: List[CoreObjectInterface]):
        self._core_function = {}
        self._core = []
        for core in core_object:
            self._core.append(core)
            core.set_executor(self)
            for function_name in core.get_all_functions():
                if function_name in self._core_function:
                    fn = function_name
                    c1 = core
                    c2 = self._core_function[function_name]
                    raise ExecutorFunctionAlreadyExistError(
                        f"'{fn}' from '{c1}' in '{c2}'")
                self._core_function[function_name] = core

    def execute_line(self, line: List[str]):
        if line[0] not in self._core_function:
            raise ExecutorFunctionNotExistError(
                f"'{line[0]}' not exist in '{self}'")
        return self._core_function[line[0]].execute(line[0], *line[1:])

    def execute(self, script: List[List[str]]) -> Any:
        self.stop = False
        result = None
        for line in script:
            result = self.execute_line(line)
            if self.stop:
                break
        return result
