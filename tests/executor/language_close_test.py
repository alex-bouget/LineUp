import unittest
from timeout_decorator import timeout
from ddt import ddt, data
from tests.mocks import CoreObjectCloseMock
from lineup_lang import Language, luexec


@ddt
class LanguageCloseTest(unittest.TestCase):

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close(self, executor):
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
        obj = CoreObjectCloseMock()
        with Language(executor([obj]), False) as _:
            pass
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)

    @timeout(2)
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close_with_lang_deletion(self, executor):
        obj = CoreObjectCloseMock()
        lang = Language(executor([obj]), False)
        self.assertFalse(obj._is_closed)
        self.assertEqual(obj.nb_close, 0)
        del lang
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)
