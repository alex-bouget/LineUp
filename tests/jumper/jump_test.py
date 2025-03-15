import unittest
from timeout_decorator import timeout
from lineup_lang import Language, luexec
from tests.mocks import FakeExitObject


class JumpTest(unittest.TestCase):
    @timeout(2)
    def test_new_jump(self):
        language = Language(luexec.JumperExecutor([FakeExitObject()]))
        # instruction 0 executed
        self.assertEqual(language.execute_script("EXIT"), 0)
        # Jump 1 line after myself (instruction 2)
        self.assertEqual(language.execute_script("NOTHING\nJUMP 1\nEXIT\nEXIT"), 2)
        # From line 5, jump back 2 lines (line 3 so instruction 2)
        self.assertEqual(language.execute_script("GOTO 5\nEXIT\nEXIT\nEXIT\nJUMP -2\nEXIT"), 2)

    @timeout(2)
    def test_goto(self):
        language = Language(luexec.JumperExecutor([FakeExitObject()]))
        # instruction 0 executed
        self.assertEqual(language.execute_script("EXIT"), 0)
        # Jump to the line 3 (instruction 2)
        self.assertEqual(language.execute_script("NOTHING\nGOTO 3\nEXIT\nEXIT"), 2)
        # Jump 1 line after myself (instruction 2)
        # From line 5, jump back 2 lines (line 3 so instruction 2)
        self.assertEqual(language.execute_script("GOTO 5\nEXIT\nEXIT\nEXIT\nEXIT\nEXIT"), 4)
