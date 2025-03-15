import unittest
from timeout_decorator import timeout
from lineup_lang.line_decoder import LineDecoder
from lineup_lang.error import DecodeLineStringError


class DecoderTest(unittest.TestCase):
    """
    A decoder test class for the LineDecoder class.

    - Need to test:
      - Splitting the line along the spaces.
      - If token is empty, delete it.

      - If a token is quoted, keep it as a single token.
      - If a token is quoted, remove the quotes.
      - If a token is quoted, keep the spaces inside the quotes.
      - If a token is quoted, but sticked to the next token, it's considered like a space between them.
      - If a token is quoted, but sticked to the previous token, it's considered like a space between them.

      - TODO A token quoted is a JSON string.

      - If a hashtag is found, ignore the rest of the line.
      - An hashtag can be escaped with a backslash.
      - A quote can be escaped with a backslash.
      - If a backslash is used for escaping, remove it.
      - If a backslash is used for escaping, keep the character after it.
      - If a backslash is used for escaping, it can be escaped with another backslash.
      - A bad line should raise an error.
      - If a line is empty, return None.
    """
    @timeout(2)
    def test_decode(self):
        line = LineDecoder()
        # Splitting the line along the spaces.
        self.assertEqual(line.decode("1 2 3 4"), ["1", "2", "3", "4"])
        # If token is empty, delete it.
        self.assertEqual(line.decode("1   2  3 4 5"), ["1", "2", "3", "4", "5"])

    @timeout(2)
    def test_decode_with_quotes(self):
        line = LineDecoder()
        # If a token is quoted, keep it as a single token.
        # If a token is quoted, remove the quotes.
        # If a token is quoted, keep the spaces inside the quotes.
        self.assertEqual(line.decode('1 "2 3" 4'), ["1", "2 3", "4"])
        self.assertEqual(line.decode('1    "2 3" 4'), ["1", "2 3", "4"])
        self.assertEqual(line.decode('1 "2    3" 4'), ["1", "2    3", "4"])
        # If a token is quoted, but sticked to the next token, it's considered like a space between them.
        # If a token is quoted, but sticked to the previous token, it's considered like a space between them.
        self.assertEqual(line.decode('$"a"$'), ["$", "a", "$"])

    @timeout(2)
    def test_decode_with_comment(self):
        line = LineDecoder()
        # If a hashtag is found, ignore the rest of the line.
        self.assertEqual(line.decode('1 2 3 4 #5'), ["1", "2", "3", "4"])
        self.assertEqual(line.decode('1 2 3 4 # 5'), ["1", "2", "3", "4"])
        self.assertEqual(line.decode('1 #2 3 4 5'), ["1"])
        self.assertEqual(line.decode('1   2    # 2 3 4 5'), ["1", "2"])

    @timeout(2)
    def test_escaped(self):
        line = LineDecoder()
        # If a backslash is used for escaping, remove it.
        # If a backslash is used for escaping, keep the character after it.

        # An hashtag can be escaped with a backslash.
        self.assertEqual(line.decode('1 \\#3 4'), ["1", "#3", "4"])
        # A quote can be escaped with a backslash.
        self.assertEqual(line.decode('1 "2 \\"3" 4'), ["1", '2 "3', "4"])
        self.assertEqual(line.decode('1 \\"3 4'), ["1", '"3', "4"])
        self.assertEqual(line.decode('1 "\\3" 4'), ["1", '\\3', "4"])
        # The backslash is not used for escaping.
        self.assertEqual(line.decode('1 \\\\3 4'), ["1", "\\\\3", "4"])

        # If a backslash is used for escaping, it can be escaped with another backslash.
        self.assertEqual(line.decode('1 \\\\"3" 4'), ["1", "\\", "3", "4"])
        self.assertEqual(line.decode('1 "5 \\\\"3 4'), ["1", "5 \\", "3", "4"])

        # Three backslashes and a quote.
        # The first backslash is used for escaping the second backslash.
        # The third backslash is used for escaping the quote.
        self.assertEqual(line.decode('1 \\\\\\"3 4'), ["1", '\\"3', "4"])

    @timeout(2)
    def test_error(self):
        line = LineDecoder()
        # A bad line should raise an error.
        with self.assertRaises(DecodeLineStringError):
            line.decode('1 "2 3')
        with self.assertRaises(DecodeLineStringError):
            line.decode('1 "2 3\\"')
        with self.assertRaises(DecodeLineStringError):
            line.decode('1 "2 3\\" 4')

    @timeout(2)
    def test_limit_case(self):
        line = LineDecoder()
        # If a line is empty, return None.
        self.assertIsNone(line.decode(''))
        self.assertIsNone(line.decode('    '))
        self.assertIsNone(line.decode('    #'))
        self.assertIsNone(line.decode('    # '))
