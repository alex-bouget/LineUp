import unittest
from timeout_decorator import timeout
from tests.mocks import LanguageObjectMock, CoreObjectMock
from lineup_lang import Language, lucore, luexec


class VariableActionLanguageTest(unittest.TestCase):
    """
    This class tests the variable actions.
    In particular, the actions on language objects in variables.
    See variable_action_test.py for more information.


    4. USE
        - Use a result from a core function for set a variable
    5. EXEC
        - Execute a function in a language object
        - same as ... but with a function for the function who can be hide by a variable function (GET, SET, ...)
    6. ...
        - Execute a function in a language object
        - same as EXEC
    """
    @timeout(2)
    def test_execution(self):
        default_variables = {"VAR1": 1, "VAR2": LanguageObjectMock()}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR1 GET"), 1)
        # Test the ... EXEC action
        self.assertEqual(language.execute_script("VAR VAR2 FUNC1"), 51)
        self.assertEqual(language.execute_script("VAR VAR2 EXEC FUNC1"), 51)
        # Test the USE action
        self.assertEqual(language.execute_script("VAR VAR3 USE VAR VAR2 FUNC1\nVAR VAR3 GET"), 51)

    @timeout(2)
    def test_execution_reset(self):
        # Test the reset of a language object in a variable
        obj = LanguageObjectMock()
        default_variables = {"VAR1": 1, "VAR2": obj}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables)]), False)
        self.assertEqual(language.execute_script("VAR VAR2 BUILD 10\nVAR VAR2 EXEC GET"), 10)
        self.assertEqual(obj.x, 0)
        self.assertEqual(language.execute_script("VAR VAR2 EXEC GET"), 0)

    @timeout(2)
    def test_execution_core(self):
        # Test the USE action with a core object
        core = CoreObjectMock()
        obj = LanguageObjectMock()
        default_variables = {"VAR1": 1, "VAR2": obj}
        language = Language(luexec.DefaultExecutor([lucore.Variables(default_variables), core]), False)
        self.assertEqual(language.execute_script("VAR VAR3 USE GET\nVAR VAR3 GET"), 0)
        self.assertEqual(language.execute_script("BUILD 10\nVAR VAR3 USE GET\nVAR VAR3 GET"), 10)
