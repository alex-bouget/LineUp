import unittest
from timeout_decorator import timeout
from lineup_lang import Language, luexec
from lineup_lang.executor.jump import JumperOffsetInvalidError
from tests.mocks import FakeExitObject


class JumpTest(unittest.TestCase):
    """
    A test class for the JumperExecutor.

    - Need to test:
        - If the JUMP instruction is executed, the executor should execute the line set in the argument from the current line.
        - If the JUMP argument is negative, the executor should jump back to the previous line.
        - If the JUMP argument is zero, an error should be thrown.
        - If the GOTO instruction is executed, the executor should execute the line set in the argument.
        - If the GOTO argument is negative or zero, an error should be thrown.
    """

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

    @timeout(2)
    def test_goto_zero_error(self):
        language = Language(luexec.JumperExecutor([FakeExitObject()]), False)
        with self.assertRaises(JumperOffsetInvalidError):
            language.execute_script("GOTO 0")

    @timeout(2)
    def test_jump_zero_error(self):
        language = Language(luexec.JumperExecutor([FakeExitObject()]), False)
        with self.assertRaises(JumperOffsetInvalidError):
            language.execute_script("JUMP 0")

    @timeout(2)
    def test_goto_negative_error(self):
        language = Language(luexec.JumperExecutor([FakeExitObject()]), False)
        with self.assertRaises(JumperOffsetInvalidError):
            language.execute_script("GOTO -1")
