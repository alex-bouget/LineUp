from lineup_lang import CoreObjectInterface, LanguageObjectInterface
from typing import List


class FakeExitObject(CoreObjectInterface):
    def __init__(self):
        self.functions = {
            "NOTHING": lambda *args: None,
            "EXIT": self.fake_exit
        }

    def fake_exit(self, *args):
        self.executor.stopped = True
        # Return the last execution line executed
        return self.executor.line


class CoreObjectCloseMock(CoreObjectInterface):
    nb_close = 0

    functions = {}

    def close(self):
        self.nb_close += 1
        return super().close()


class CoreObjectResetMock(CoreObjectInterface):
    nb_reset = 0

    def __init__(self):
        super().__init__()
        self.functions = {"FUNC1": lambda: self.nb_reset}

    def reset(self):
        self.nb_reset += 1
        return super().reset()


class CoreObjectFunctionMock(CoreObjectInterface):
    func_called: List[str] = []

    def __init__(self):
        self.functions = {
            "FUNC1": self._func1,
            "FUNC2": self._func2,
        }

    def _func1(self, *args):
        self.func_called.append("FUNC1")
        return "FUNC1"

    def _func2(self, *args):
        self.func_called.append("FUNC2")
        return None


class LanguageObjectMock(LanguageObjectInterface):
    x: int = 0

    def __init__(self):
        self.x = 0
        self.functions = {
            "FUNC1": lambda: 51,
            "BUILD": self._build,
            "GET": self._get,
        }

    def _build(self, x: str):
        self.x = int(x)

    def _get(self):
        return self.x

    def reset(self):
        self.x = 0
        return super().reset()


class CoreObjectMock(CoreObjectInterface, LanguageObjectMock):
    """We use the LanguageObjectMock because it have the same functions"""
    pass