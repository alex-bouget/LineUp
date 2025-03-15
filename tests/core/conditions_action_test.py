import unittest
from timeout_decorator import timeout
from tests.mocks import FakeExitObject
from lineup_lang import Language, lucore, luexec


class ConditionsActionTest(unittest.TestCase):
    """
    This class tests the conditions actions.

    1. IF
    2. NOTIF
        - First argument is the number to go to if the condition is True/False
        - If the first argument start with a *, it will be added to the current position (JUMP instead of GOTO)

        - If the third argument is a equal sign, it will compare the argument two and four
        - else, the other argument will be executed by the executor and compared to True/False
    3. IF ELSE
        - If the last condition is not fulfilled, it will go to the number after the ELSE
        - If the argument start with a *, it will be added to the current position (JUMP instead of GOTO)
    """

    @timeout(2)
    def test_if(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        # GOTO 3 if VAR3 is None
        self.assertEqual(language.execute_script('IF 3 VAR VAR3 GET\nEXIT\nEXIT\nEXIT'), 1)
        # GOTO 3 if VAR1 is equal to VAR2
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" EQ "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 2)
        # GOTO 3 if VAR1 is not equal to VAR2
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" NE "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 1)

    @timeout(2)
    def test_not_if(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        # GOTO 3 if VAR3 is not None
        self.assertEqual(language.execute_script('NOTIF 3 VAR VAR3 GET\nEXIT\nEXIT\nEXIT'), 2)
        # GOTO 3 if VAR1 is equal to VAR2
        self.assertEqual(language.execute_script('NOTIF 3 "VAR VAR1 GET" EQ "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 1)
        # GOTO 3 if VAR1 is not equal to VAR2
        self.assertEqual(language.execute_script('NOTIF 3 "VAR VAR1 GET" NE "VAR VAR2 GET"\nEXIT\nEXIT\nEXIT'), 2)

    @timeout(2)
    def test_if_else(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        # GOTO 3 if VAR3 is None else GOTO 4
        self.assertEqual(language.execute_script('IF 3 VAR VAR3 GET\nELSE 4\nEXIT\nEXIT\nEXIT'), 1)
        # GOTO 3 if VAR1 is equal to VAR2 else GOTO 4
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" EQ "VAR VAR2 GET"\nELSE 4\nEXIT\nEXIT\nEXIT'), 3)
        # GOTO 3 if VAR1 is not equal to VAR2 else GOTO 4
        self.assertEqual(language.execute_script('IF 3 "VAR VAR1 GET" NE "VAR VAR2 GET"\nELSE 4\nEXIT\nEXIT\nEXIT'), 1)

    @timeout(2)
    def test_jump_not_goto(self):
        variables = lucore.Variables({"VAR1": 1, "VAR2": 1, "VAR3": None})
        conditions = lucore.Conditions()
        language = Language(luexec.DefaultExecutor([FakeExitObject(), variables, conditions]), False)
        # JUMP 3 if VAR3 is None
        self.assertEqual(language.execute_script('NOTHING\nIF *+3 VAR VAR3 GET\nELSE 4\nEXIT\nEXIT\nEXIT'), 4)
