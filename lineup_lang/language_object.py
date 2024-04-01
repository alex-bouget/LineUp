from typing import Dict, Any, Callable, List
from .error import FunctionNotExistError


class LanguageObjectInterface:
    functions: Dict[str, Callable[..., Any]]

    def get_all_functions(self) -> List[str]:
        return list(self.functions.keys())

    def execute(self, function_name: str, *args) -> Any:
        if function_name not in self.functions:
            raise FunctionNotExistError(
                f"'{function_name}' not exist in '{self}'")
        return self.functions[function_name](*args)

    def close(self):
        pass

    def reset(self):
        pass

    def __str__(self) -> str:
        return f"<LUPO:{self.__class__.__name__}>"


class CoreObjectInterface(LanguageObjectInterface):
    executor: Any

    def set_executor(self, executor: Any) -> None:
        self.executor = executor

    def __str__(self) -> str:
        return f"<LUPC:{self.__class__.__name__}>"


class LanguageExecutorInterface:
    _core_function: Dict[str, LanguageObjectInterface]
    _core: List[LanguageObjectInterface]

    def execute_line(self, line: List[str]):
        pass

    def execute(self, script: List[List[str]]) -> Any:
        pass

    def close(self) -> None:
        for core in self._core:
            core.close()

    def reset(self) -> None:
        for core in self._core:
            core.reset()

    def __str__(self) -> str:
        return f"<LUPE:{self.__class__.__name__}>"


class LanguageInterface:
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
