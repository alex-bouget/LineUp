import unittest
from ddt import ddt, data
from lineup_lang import Language, CoreObjectInterface, luexec


class CoreObjectCloseMock(CoreObjectInterface):
    nb_close = 0

    functions = {}

    def close(self):
        self.nb_close += 1
        return super().close()


@ddt
class LanguageCloseTest(unittest.TestCase):

    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close(self, executor):
        obj = CoreObjectCloseMock()
        lang = Language(executor([obj]))
        lang.close()
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)
        lang.close()
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)

    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close_with(self, executor):
        obj = CoreObjectCloseMock()
        with Language(executor([obj])) as _:
            pass
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)

    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_close_with_lang_deletion(self, executor):
        obj = CoreObjectCloseMock()
        lang = Language(executor([obj]))
        self.assertFalse(obj._is_closed)
        self.assertEqual(obj.nb_close, 0)
        del lang
        self.assertTrue(obj._is_closed)
        self.assertEqual(obj.nb_close, 1)
