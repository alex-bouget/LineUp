import unittest
from typing import List
from ddt import ddt, data
from lineup_lang import luexec
from lineup_lang.error import ExecutorFunctionNotExistError
from lineup_lang import CoreObjectInterface, LanguageExecutorInterface


class CoreObjectMock(CoreObjectInterface):
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


@ddt
class CoreExecutionTest(unittest.TestCase):
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_executor(self, executor):
        obj = CoreObjectMock()
        obj.func_called = []
        executor: LanguageExecutorInterface = executor([obj])
        self.assertEqual(executor.execute_line(["FUNC1"]), "FUNC1")
        self.assertEqual(obj.func_called, ["FUNC1"])
        obj.func_called = []
        self.assertEqual(executor.execute_line(["FUNC2"]), None)
        self.assertEqual(obj.func_called, ["FUNC2"])
        obj.func_called = []

        with self.assertRaises(ExecutorFunctionNotExistError):
            executor.execute_line(["FUNC3"])

    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def text_execute_all_function(self, executor):
        obj = CoreObjectMock()
        obj.func_called = []
        executor: LanguageExecutorInterface = executor([obj])
        self.assertEqual(executor.execute([["FUNC1"], ["FUNC2"]]), None)
        self.assertEqual(obj.func_called, ["FUNC1", "FUNC2"])
        obj.func_called = []

        with self.assertRaises(ExecutorFunctionNotExistError):
            executor.execute([["FUNC1"], ["FUNC3"]])

        with self.assertRaises(ExecutorFunctionNotExistError):
            executor.execute([["FUNC3", "FUNC1"]])
