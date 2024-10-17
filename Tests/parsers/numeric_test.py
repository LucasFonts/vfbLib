from unittest import TestCase
from vfbLib.parsers.numeric import (
    IntParser,
    # Int32Parser,
    Int64Parser,
    SignedIntParser,
    SignedInt32Parser,
)
from vfbLib.testhelpers import expect


class IntParserTest(TestCase):
    def test_unicode_ranges(self):
        expect(IntParser, "3200", 50)


class Int64ParserTest(TestCase):
    def test_unicode_ranges(self):
        expect(Int64Parser, "00000000000000000000000000000000", 0)


class SignedIntParserTest(TestCase):
    def test_minus_one(self):
        expect(SignedIntParser, "ffff", -1)

    def test_hhea_ascender(self):
        expect(SignedIntParser, "ee02", 750)

    def test_hhea_descender(self):
        expect(SignedIntParser, "06ff", -250)


class SignedInt32ParserTest(TestCase):
    def test_minus_one(self):
        expect(SignedInt32Parser, "ffffffff", -1)
