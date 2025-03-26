import io
import sys
import unittest
from timeout_decorator import timeout
from lineup_lang import Language, lucore, luexec


class SystemActionTest(unittest.TestCase):
    """
    This class tests the system actions.

    EXIT: Exit the program and return a value executed by an action.
    DEBUG: Print a value or execute an action and print the result.
    OBJ: Return the object passed as argument.
    """

    def start_capture(self):
        capturedOutput = io.StringIO()                 # Create StringIO.
        sys.stdout = capturedOutput                    # Redirect stdout.

    def end_capture(self):
        value = sys.stdout.getvalue()                  # Get captured output.
        sys.stdout = sys.__stdout__                    # Reset redirect.
        return value

    @timeout(2)
    def test_exit(self):
        system = lucore.System()
        variables = lucore.Variables({"VAR1": 1, "VAR2": 51, "VAR3": None})
        language = Language(luexec.JumperExecutor([variables, system]), False)
        # Return nothing
        self.assertIsNone(language.execute_script('EXIT'))
        self.assertIsNone(language.execute_script('EXIT\nEXIT\nEXIT'))
        # Return a value
        self.assertEqual(language.execute_script('EXIT VAR VAR1 GET'), 1)
        self.assertEqual(language.execute_script('EXIT VAR VAR2 GET'), 51)

    @timeout(2)
    def test_debug(self):
        system = lucore.System()
        variables = lucore.Variables({"VAR1": 1, "VAR2": 51, "VAR3": None})
        language = Language(luexec.JumperExecutor([variables, system]), False)
        self.start_capture()
        language.execute_script('DEBUG "Hello World"')
        self.assertEqual(self.end_capture(), "Hello World\n")
        self.start_capture()
        language.execute_script('DEBUG VAR VAR1 GET')
        self.assertEqual(self.end_capture(), "1\n")
        self.start_capture()
        language.execute_script('DEBUG VAR VAR2 GET')
        self.assertEqual(self.end_capture(), "51\n")
        self.start_capture()
        language.execute_script('DEBUG')
        self.assertEqual(self.end_capture(), "DEBUG\n")

    @timeout(2)
    def test_obj(self):
        system = lucore.System()
        language = Language(luexec.JumperExecutor([system]), False)
        self.assertEqual(language.execute_script('OBJ "Hello World"'), "Hello World")
        self.assertEqual(language.execute_script('OBJ VAR VAR1 GET'), ("VAR", "VAR1", "GET"))
        self.assertEqual(language.execute_script('OBJ 1 2 3'), ("1", "2", "3"))
        self.assertEqual(language.execute_script('OBJ 1'), "1")
