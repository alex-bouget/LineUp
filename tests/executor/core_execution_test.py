import unittest
from timeout_decorator import timeout
from ddt import ddt, data
from tests.mocks import CoreObjectFunctionMock
from lineup_lang import luexec, LanguageExecutorInterface
from lineup_lang.error import ExecutorFunctionNotExistError


@ddt
class CoreExecutionTest(unittest.TestCase):
    """
    A test class for the Core execution method.

    - Need to test:
        - If the executor can execute a function.
        - If the executor can execute multiple functions.
        - If the executor can't execute a function that does not exist.
    """
    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_executor(self, executor):
        # If the executor can execute a function.
        obj = CoreObjectFunctionMock()
        obj.func_called = []
        executor: LanguageExecutorInterface = executor([obj])
        self.assertEqual(executor.execute_line(["FUNC1"]), "FUNC1")
        self.assertEqual(obj.func_called, ["FUNC1"])
        obj.func_called = []
        self.assertIsNone(executor.execute_line(["FUNC2"]))
        self.assertEqual(obj.func_called, ["FUNC2"])
        obj.func_called = []

        with self.assertRaises(ExecutorFunctionNotExistError):
            executor.execute_line(["FUNC3"])

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_execute_all_function(self, executor):
        # If the executor can execute multiple functions.
        obj = CoreObjectFunctionMock()
        obj.func_called = []
        executor: LanguageExecutorInterface = executor([obj])
        self.assertIsNone(executor.execute([["FUNC1"], ["FUNC2"]]))
        self.assertEqual(obj.func_called, ["FUNC1", "FUNC2"])
        obj.func_called = []

        # If the executor can't execute a function that does not exist.
        with self.assertRaises(ExecutorFunctionNotExistError):
            executor.execute([["FUNC1"], ["FUNC3"]])

        with self.assertRaises(ExecutorFunctionNotExistError):
            executor.execute([["FUNC3", "FUNC1"]])
