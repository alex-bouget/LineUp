import unittest
from timeout_decorator import timeout
from lineup_lang.args_resolver import ArgsResolver


class ArgsResolverTest(unittest.TestCase):
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
