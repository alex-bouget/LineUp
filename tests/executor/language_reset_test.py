import unittest
from timeout_decorator import timeout
from ddt import ddt, data
from tests.mocks import CoreObjectResetMock
from lineup_lang import Language, luexec
from lineup_lang.error import AlreadyClosedError


@ddt
class LanguageResetTest(unittest.TestCase):
    """
    A test class for the Language reset method.

    - Need to test:
        - If the reset method is called, the executor should reset all the objects it uses.
        - If the reset method is called multiple times, the executor should reset the objects multiple times.
        - The reset method should be called after the execution of a script.
        - The reset method can't be called after the close method.
    """
    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_reset(self, executor):
        # If the reset method is called, the executor should reset all the objects it uses.
        # If the reset method is called multiple times, the executor should reset the objects multiple times.
        obj = CoreObjectResetMock()
        lang = Language(executor([obj]), False)
        lang.reset()
        self.assertEqual(obj.nb_reset, 1)
        lang.reset()
        self.assertEqual(obj.nb_reset, 2)

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_reset_after_execution(self, executor):
        # The reset method should be called after the execution of a script.
        obj = CoreObjectResetMock()
        lang = Language(executor([obj]), False)
        result = lang.execute_script("FUNC1")
        self.assertEqual(obj.nb_reset, 1)
        self.assertEqual(result, 0)

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_reset_after_close(self, executor):
        # The reset method can't be called after the close method
        obj = CoreObjectResetMock()
        lang = Language(executor([obj]), False)
        lang.close()
        with self.assertRaises(AlreadyClosedError):
            lang.reset()
        self.assertEqual(obj.nb_reset, 0)
