import unittest
from timeout_decorator import timeout
from lineup_lang.line_decoder import LineDecoder
from lineup_lang.error import DecodeLineStringError


class DecoderTest(unittest.TestCase):
    @timeout(2)
    def test_decode(self):
        line = LineDecoder()
        self.assertEqual(line.decode("1 2 3 4"), ["1", "2", "3", "4"])
        self.assertEqual(line.decode("1   2  3 4 5"), ["1", "2", "3", "4", "5"])

    @timeout(2)
    def test_decode_with_quotes(self):
        line = LineDecoder()
        self.assertEqual(line.decode('1 "2 3" 4'), ["1", "2 3", "4"])
        self.assertEqual(line.decode('1    "2 3" 4'), ["1", "2 3", "4"])
        self.assertEqual(line.decode('1 "2    3" 4'), ["1", "2    3", "4"])

    @timeout(2)
    def test_decode_with_comment(self):
        line = LineDecoder()
        self.assertEqual(line.decode('1 2 3 4 #5'), ["1", "2", "3", "4"])
        self.assertEqual(line.decode('1 2 3 4 # 5'), ["1", "2", "3", "4"])
        self.assertEqual(line.decode('1 #2 3 4 5'), ["1"])
        self.assertEqual(line.decode('1   2    # 2 3 4 5'), ["1", "2"])

    @timeout(2)
    def test_limit_case(self):
        line = LineDecoder()
        self.assertIsNone(line.decode(''))
        self.assertIsNone(line.decode('    '))
        self.assertIsNone(line.decode('    #'))
        self.assertIsNone(line.decode('    # '))
        self.assertEqual(line.decode('$"a"'), ["$", "a"])

    @timeout(2)
    def test_escaped(self):
        line = LineDecoder()
        self.assertEqual(line.decode('1 "2 \\"3" 4'), ["1", '2 "3', "4"])
        self.assertEqual(line.decode('1 \\"3 4'), ["1", '"3', "4"])
        self.assertEqual(line.decode('1 "\\3" 4'), ["1", '\\3', "4"])
        self.assertEqual(line.decode('1 \\#3 4'), ["1", "#3", "4"])
        self.assertEqual(line.decode('1 \\\\3 4'), ["1", "\\\\3", "4"])
        self.assertEqual(line.decode('1 \\\\"3" 4'), ["1", "\\", "3", "4"])
        self.assertEqual(line.decode('1 \\\\\\"3 4'), ["1", '\\"3', "4"])
        self.assertEqual(line.decode('1 "5 \\\\"3 4'), ["1", "5 \\", "3", "4"])

    @timeout(2)
    def test_error(self):
        line = LineDecoder()
        with self.assertRaises(DecodeLineStringError):
            line.decode('1 "2 3')
        with self.assertRaises(DecodeLineStringError):
            line.decode('1 "2 3\\"')
        with self.assertRaises(DecodeLineStringError):
            line.decode('1 "2 3\\" 4')
