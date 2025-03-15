import unittest
from timeout_decorator import timeout
from tests.mocks import FakeExitObject
from lineup_lang import Language, lucore, luexec


class ConditionsActionTest(unittest.TestCase):
    @timeout(2)
    def test_if(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        self.assertEqual(language.execute_script('IF 3 VAR VAR3 GET\nEXIT\nEXIT\nEXIT'), 1)
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" EQ "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 2)
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" NE "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 1)

    @timeout(2)
    def test_not_if(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        self.assertEqual(language.execute_script('NOTIF 3 VAR VAR3 GET\nEXIT\nEXIT\nEXIT'), 2)
        self.assertEqual(language.execute_script('NOTIF 3 "VAR VAR1 GET" EQ "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 1)
        self.assertEqual(language.execute_script('NOTIF 3 "VAR VAR1 GET" NE "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 2)

    @timeout(2)
    def test_if_else(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        self.assertEqual(language.execute_script('IF 3 VAR VAR3 GET\nELSE 4\nEXIT\nEXIT\nEXIT'), 1)
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" EQ "VAR VAR2 GET"\nELSE 4\nEXIT\nEXIT\nEXIT'), 3)
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" NE "VAR VAR2 GET"\nELSE 4\nEXIT\nEXIT\nEXIT'), 1)

    @timeout(2)
    def test_jump_not_goto(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        self.assertEqual(language.execute_script('NOTHING\nIF *+3 VAR VAR3 GET\nELSE 4\nEXIT\nEXIT\nEXIT'), 4)
