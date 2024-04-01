from typing import List, Any
from .language_object import LanguageInterface, LanguageExecutorInterface, \
     LanguageObjectInterface
from .error import ArgumentNotExistError, DecodeLineStringError, LineupError
from .logger import start_logging
import lineup_lang.executor as luexec
import lineup_lang.core as lucore
import regex as re
import logging

__all__ = ["Language", "LanguageObjectInterface", "luexec", "lucore"]


class Language(LanguageInterface):
    _executor: LanguageExecutorInterface
    no_error: bool
    logger = logging.getLogger("lineup_lang")

    def __init__(self, executor: LanguageExecutorInterface,
                 no_error: bool = True, log_level: str = "WARN"):
        start_logging(log_level)
        logger = logging.getLogger("lineup_lang")
        self._executor = executor
        self.no_error = no_error

    def _resolve_line(self, line: str):
        lines = line.split(" ")
        result = []
        tmp = ""
        for data in lines:
            if data.startswith('"') and data.endswith('"'):
                result.append("".join(data[1:-1]))
            elif data.startswith('"'):
                if tmp:
                    raise DecodeLineStringError(
                        f"'{line}' is not valid line string")
                tmp = data
            elif data.endswith('"'):
                if not tmp:
                    raise DecodeLineStringError(
                        f"'{line}' is not valid line string")
                tmp += " " + data
                result.append("".join(tmp[1:-1]))
                tmp = ""
            elif tmp:
                tmp += " " + data
            else:
                result.append(data)
        if tmp:
            raise DecodeLineStringError(
                f"'{line}' is not valid line string")
        return result

    def _get_line(self, line: str) -> List[str] | None:
        line = line.strip()
        if not line:
            return None
        if line.startswith("#"):
            return None
        return self._resolve_line(line)

    def _resolve_args(self, script: str, **kwargs):
        regex = r"\$(\((\w+):(.+?)\)|(\w+))"
        matches = re.finditer(regex, script)
        for match in matches:
            keyname = match.group(2) or match.group(4)
            default_value = match.group(3)
            if keyname in kwargs:
                value = kwargs[keyname]
            elif default_value is None:
                raise ArgumentNotExistError(
                    f"'{keyname}' not exist in '{kwargs}'")
            else:
                value = default_value
            script = script.replace(match.group(0), "\"" + value + "\"")
        return script

    def close(self):
        self._executor.close()

    def execute_script(self, script: str) -> Any:
        self.logger.debug(f"Execute script:\n{script}")
        script_lines = []
        for line in script.split("\n"):
            line = self._get_line(line)
            if line:
                script_lines.append(line)
        try:
            result = self._executor.execute(script_lines)
        except LineupError as e:
            if self.no_error:
                return e
            raise e
        self._executor.reset()
        return result

    def execute_script_with_args(self, script: str, **kwargs) -> Any:
        script = self._resolve_args(script, **kwargs)
        return self.execute_script(script)

    def execute_file(self, file_path: str, **kwargs) -> Any:
        with open(file_path, "r") as file:
            script = file.read()
        return self.execute_script_with_args(script, **kwargs)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"
