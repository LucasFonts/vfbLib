from unittest import TestCase
from vfbLib.parsers.numeric import (
    IntParser,
    # Int32Parser,
    Int64Parser,
    SignedIntParser,
    SignedInt32Parser,
)


class IntParserTest(TestCase):
    def test_unicode_ranges(self):
        data = "3200"
        expected = 50
        result = IntParser().parse_hex(data)
        assert result == expected


class Int64ParserTest(TestCase):
    def test_unicode_ranges(self):
        data = "00000000000000000000000000000000"
        expected = 0
        result = Int64Parser().parse_hex(data)
        assert result == expected


class SignedIntParserTest(TestCase):
    def test_minus_one(self):
        data = "ffff"
        expected = -1
        result = SignedIntParser().parse_hex(data)
        assert result == expected

    def test_hhea_ascender(self):
        data = "ee02"
        expected = 750
        result = SignedIntParser().parse_hex(data)
        assert result == expected

    def test_hhea_descender(self):
        data = "06ff"
        expected = -250
        result = SignedIntParser().parse_hex(data)
        assert result == expected


class SignedInt32ParserTest(TestCase):
    def test_minus_one(self):
        data = "ffffffff"
        expected = -1
        result = SignedInt32Parser().parse_hex(data)
        assert result == expected
