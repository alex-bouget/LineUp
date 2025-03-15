import unittest
from timeout_decorator import timeout
from tests.mocks import LanguageObjectMock, CoreObjectMock
from lineup_lang import Language, lucore, luexec


class VariableActionLanguageTest(unittest.TestCase):
    @timeout(2)
    def test_execution(self):
        default_variables = {"VAR1": 1, "VAR2": LanguageObjectMock()}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        self.assertEqual(language.execute_script("VAR VAR2 FUNC1"), 51)
        self.assertEqual(language.execute_script("VAR VAR2 EXEC FUNC1"), 51)
        self.assertEqual(language.execute_script("VAR VAR3 USE VAR VAR2 FUNC1\nVAR VAR3 GET"), 51)

    @timeout(2)
    def test_execution_reset(self):
        obj = LanguageObjectMock()
        default_variables = {"VAR1": 1, "VAR2": obj}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR2 BUILD 10\nVAR VAR2 EXEC GET"), 10)
        self.assertEqual(obj.x, 0)
        self.assertEqual(language.execute_script("VAR VAR2 EXEC GET"), 0)

    @timeout(2)
    def test_execution_core(self):
        core = CoreObjectMock()
        obj = LanguageObjectMock()
        default_variables = {"VAR1": 1, "VAR2": obj}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables), core]), False)
        self.assertEqual(language.execute_script("VAR VAR3 USE GET\nVAR VAR3 GET"), 0)
        self.assertEqual(language.execute_script("BUILD 10\nVAR VAR3 USE GET\nVAR VAR3 GET"), 10)
