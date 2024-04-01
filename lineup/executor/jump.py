from .default import DefaultExecutor
from ..error import ExecutorFunctionNotExistError
from typing import Any, List


class JumperExecutor(DefaultExecutor):
    jump_functions = ["JUMP"]
    line = 0

    def jump(self, line: int):
        self.line = line
        self.line -= 1

    def execute_jump(self, line: List[str]):
        if line[0] == "JUMP":
            if (len(line) > 2):
                if line[2] == "FROM":
                    self.jump(self.line + int(line[1]))
            else:
                self.jump(int(line[1]))
            return None
        raise ExecutorFunctionNotExistError(
            f"'{line[0]}' not exist in '{self}'")

    def execute_line(self, line: List[str]):
        if line[0] in self.jump_functions:
            return self.execute_jump(line)
        return super().execute_line(line)

    def execute(self, script: List[List[str]]) -> Any:
        result = None
        self.line = 0
        while self.line < len(script):
            result = self.execute_line(script[self.line])
            self.line += 1
        return result
