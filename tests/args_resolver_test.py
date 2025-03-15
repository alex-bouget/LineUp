import unittest
from timeout_decorator import timeout
from lineup_lang.args_resolver import ArgsResolver


class ArgsResolverTest(unittest.TestCase):
    """
    A test class for the ArgsResolver class.

    - Need to test:
        - If a variable is found, replace it with the value inside a double quote.
        - TODO The value is JSON encoded when it's replaced.
        - If a variable not exists, replace it with the default value in the second part of the bracket.
        - TODO If a variable not exists and no default value, throw an error.

    """
    @timeout(2)
    def test_regex_1(self):
        resolver = ArgsResolver()
        self.assertEqual(resolver.resolve("${a}", a="b"), "\"b\"")
        self.assertEqual(resolver.resolve("${a}", a="b c"), "\"b c\"")
        self.assertEqual(resolver.resolve("a ${a} c", a="b"), "a \"b\" c")
        self.assertEqual(resolver.resolve("a ${a} c", a="b c"), "a \"b c\" c")

    @timeout(2)
    def test_regex_1_with_default(self):
        resolver = ArgsResolver()
        self.assertEqual(resolver.resolve("${a:default}", a="b"), "\"b\"")
        self.assertEqual(resolver.resolve("${a:default}"), "\"default\"")
        self.assertEqual(resolver.resolve("a ${a:default} c", a="b"), "a \"b\" c")
        self.assertEqual(resolver.resolve("a ${a:default} c"), "a \"default\" c")

    @timeout(2)
    def test_regex_2(self):
        resolver = ArgsResolver()
        self.assertEqual(resolver.resolve("$a", a="b"), "\"b\"")
        self.assertEqual(resolver.resolve("$a", a="b c"), "\"b c\"")
        self.assertEqual(resolver.resolve("a $a c", a="b"), "a \"b\" c")
        self.assertEqual(resolver.resolve("a $a c", a="b c"), "a \"b c\" c")

    @timeout(2)
    def test_complicated_case(self):
        resolver = ArgsResolver()
        self.assertEqual(resolver.resolve("a ${a} c $b d ${c:default} e", a='"', b="b", c="c"), """a "\\"" c "b" d "c" e""")
        self.assertEqual(resolver.resolve("a ${a} # c $b d ${c:default} e", a='#', b="b"), """a "\\#" # c "b" d "default" e""")
