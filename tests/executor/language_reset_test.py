import unittest
from ddt import ddt, data
from lineup_lang import Language, CoreObjectInterface, luexec
from lineup_lang.error import AlreadyClosedError


class CoreObjectResetMock(CoreObjectInterface):
    nb_reset = 0

    def __init__(self):
        super().__init__()
        self.functions = {"FUNC1": lambda: self.nb_reset}

    def reset(self):
        self.nb_reset += 1
        return super().reset()


@ddt
class LanguageResetTest(unittest.TestCase):
    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_reset(self, executor):
        obj = CoreObjectResetMock()
        lang = Language(executor([obj]))
        lang.reset()
        self.assertEqual(obj.nb_reset, 1)
        lang.reset()
        self.assertEqual(obj.nb_reset, 2)

    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_reset_after_execution(self, executor):
        obj = CoreObjectResetMock()
        lang = Language(executor([obj]))
        result = lang.execute_script("FUNC1")
        self.assertEqual(obj.nb_reset, 1)
        self.assertEqual(result, 0)

    @data(luexec.DefaultExecutor, luexec.JumperExecutor)
    def test_reset_after_close(self, executor):
        obj = CoreObjectResetMock()
        lang = Language(executor([obj]))
        lang.close()
        with self.assertRaises(AlreadyClosedError):
            lang.reset()
        self.assertEqual(obj.nb_reset, 0)
