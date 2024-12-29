from typing import Dict, Any, Callable, List
from .error import FunctionNotExistError
import logging


class LanguageObjectInterface:
    """
    LineUp Object with functions who can be executed by the language
    """
    functions: Dict[str, Callable[..., Any]]
    logger = logging.getLogger("lineup_lang")

    def get_all_functions(self) -> List[str]:
        """
        Get all functions name in the object
        """
        return list(self.functions.keys())

    def execute(self, function_name: str, *args) -> Any:
        """
        Execute a function in the object
        """
        if function_name not in self.functions:
            msg = f"'{function_name}' not exist in '{self}'"
            self.logger.error(msg)
            raise FunctionNotExistError(msg)
        return self.functions[function_name](*args)

    def close(self):
        """
        Destroy the object
        """
        pass

    def reset(self):
        """
        Reset the object for future new exectution
        """
        pass

    def __str__(self) -> str:
        return f"<LUPO:{self.__class__.__name__}>"


class CoreObjectInterface(LanguageObjectInterface):
    """
    Object instancied before the creation of the language executor

    Function in this object is directly accessible by the language executor
    """
    executor: Any

    def set_executor(self, executor: Any) -> None:
        self.executor = executor

    def __str__(self) -> str:
        return f"<LUPC:{self.__class__.__name__}>"


class LanguageExecutorInterface:
    """
    Language executor interface

    This object is the main object who execute the script
    It execute line each by each
    """
    _core_function: Dict[str, LanguageObjectInterface]
    _core: List[LanguageObjectInterface]

    def execute_line(self, line: List[str]):
        pass

    def execute(self, script: List[List[str]]) -> Any:
        pass

    def close(self) -> None:
        for core in self._core:
            logging.getLogger("lineup_lang").info(f"Close: {core}")
            core.close()

    def reset(self) -> None:
        for core in self._core:
            logging.getLogger("lineup_lang").info(f"Reset: {core}")
            core.reset()

    def __str__(self) -> str:
        return f"<LUPE:{self.__class__.__name__}>"


class LanguageInterface:
    """"
    Language interface
    It read the script, cut it in line and
    execute it with the language executor
    """
    def close(self):
        pass

    def execute_script(self, script: str) -> Any:
        pass

    def execute_script_with_args(self, script: str, **kwargs) -> Any:
        pass

    def execute_file(self, file_path: str, **kwargs) -> Any:
        pass

    def __str__(self) -> str:
        return f"<LUPL:{self.__class__.__name__}>"
