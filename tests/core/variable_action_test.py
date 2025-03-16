import unittest
from timeout_decorator import timeout
from lineup_lang import Language, lucore, luexec
from lineup_lang.core.variables import VariableNotExistError


class VariableActionTest(unittest.TestCase):
    """
    This class tests the variable actions.

    VAR is the action to manipulate variables.
    It has sub-actions:
    1. SET
        - Set the value of a variable
    2. UNSET
        - Delete a variable
    3. GET
        - Get the value of a variable
    4. USE
        - See variable_action_language_test.py for more information
    5. EXEC
        - See variable_action_language_test.py for more information
    6. ...
        - See variable_action_language_test.py for more information
    """
    @timeout(2)
    def test_get(self):
        # Test the GET action
        default_variables = {"VAR1": 1, "VAR2": 2}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        self.assertEqual(language.execute_script("VAR VAR2 GET"), 2)
        with self.assertRaises(VariableNotExistError):
            language.execute_script("VAR VAR3 GET")

    @timeout(2)
    def test_set(self):
        # Test the SET action
        default_variables = {"VAR1": 1, "VAR2": 2}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR3 SET 3\nVAR VAR3 GET"), "3")
        self.assertEqual(language.execute_script("VAR VAR1 SET 10\nVAR VAR1 GET"), "10")

    @timeout(2)
    def test_delete(self):
        # Test the UNSET action
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
        # Test the reset on variables
        default_variables = {"VAR1": 1, "VAR2": 2}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        language.execute_script("VAR VAR1 SET 10")
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        language.execute_script("VAR VAR3 SET 3")
        with self.assertRaises(VariableNotExistError):
            language.execute_script("VAR VAR3 GET")
