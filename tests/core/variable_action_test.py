import unittest
from timeout_decorator import timeout
from lineup_lang import Language, lucore, luexec
from lineup_lang.core.var_object import VariableNotExistError


class VariableActionTest(unittest.TestCase):
    @timeout(2)
    def test_get(self):
        default_variables = {"VAR1": 1, "VAR2": 2}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        self.assertEqual(language.execute_script("VAR VAR2 GET"), 2)
        with self.assertRaises(VariableNotExistError):
            language.execute_script("VAR VAR3 GET")

    @timeout(2)
    def test_set(self):
        default_variables = {"VAR1": 1, "VAR2": 2}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR3 SET 3\nVAR VAR3 GET"), "3")
        self.assertEqual(language.execute_script("VAR VAR1 SET 10\nVAR VAR1 GET"), "10")

    @timeout(2)
    def test_delete(self):
        default_variables = {"VAR1": 1, "VAR2": 2}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        with self.assertRaises(VariableNotExistError):
            language.execute_script("VAR VAR3 UNSET")
        with self.assertRaises(VariableNotExistError):
            language.execute_script("VAR VAR1 UNSET\nVAR VAR1 GET")
        with self.assertRaises(VariableNotExistError):
            language.execute_script("VAR VAR2 UNSET\nVAR VAR2 GET")

    @timeout(2)
    def test_execution_reset(self):
        default_variables = {"VAR1": 1, "VAR2": 2}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        language.execute_script("VAR VAR1 SET 10")
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        language.execute_script("VAR VAR3 SET 3")
        with self.assertRaises(VariableNotExistError):
            language.execute_script("VAR VAR3 GET")
