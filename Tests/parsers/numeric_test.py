from unittest import TestCase

from vfbLib.parsers.numeric import (
    Int16Parser,
    # Int32Parser,
    SignedInt16Parser,
    SignedInt32Parser,
)


class Int16ParserTest(TestCase):
    def test_unicode_ranges(self):
        data = "3200"
        expected = 50
        result = Int16Parser().parse_hex(data)
        assert result == expected


class SignedInt16ParserTest(TestCase):
    def test_minus_one(self):
        data = "ffff"
        expected = -1
        result = SignedInt16Parser().parse_hex(data)
        assert result == expected

    def test_hhea_ascender(self):
        data = "ee02"
        expected = 750
        result = SignedInt16Parser().parse_hex(data)
        assert result == expected

    def test_hhea_descender(self):
        data = "06ff"
        expected = -250
        result = SignedInt16Parser().parse_hex(data)
        assert result == expected


class SignedInt32ParserTest(TestCase):
    def test_minus_one(self):
        data = "ffffffff"
        expected = -1
        result = SignedInt32Parser().parse_hex(data)
        assert result == expected
