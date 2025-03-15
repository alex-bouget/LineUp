import unittest
from timeout_decorator import timeout
from ddt import ddt, data
from tests.mocks import CoreObjectCloseMock
from lineup_lang import Language, luexec


@ddt
class LanguageCloseTest(unittest.TestCase):
    """
    A test class for the Language close method.

    - Need to test:
        - If the close method is called, the executor should close all the objects it uses.
        - If the close method is called multiple times, the executor should only close the objects once.
        - If the Language object is deleted, it should close all the objects it uses.
    """

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close(self, executor):
        # If the close method is called, the executor should close all the objects it uses.
        # If the close method is called multiple times, the executor should only close the objects once.
        obj = CoreObjectCloseMock()
        lang = Language(executor([obj]), False)
        lang.close()
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)
        lang.close()
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close_with(self, executor):
        # If the Language object is deleted, it should close all the objects it uses.
        obj = CoreObjectCloseMock()
        with Language(executor([obj]), False) as _:
            pass
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close_with_lang_deletion(self, executor):
        # If the Language object is deleted, it should close all the objects it uses.
        obj = CoreObjectCloseMock()
        lang = Language(executor([obj]), False)
        self.assertFalse(obj._is_closed)
        self.assertEqual(obj.nb_close, 0)
        del lang
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)
