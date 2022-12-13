import pytest

from fontTools.misc.textTools import deHexStr, hexStr
from io import BytesIO
from unittest import TestCase

from vfbLib.parsers import (
    EncodedValueListParser,
    read_encoded_value,
)
from vfbLib.parsers.glyph import GlyphParser


class ValueDecoderTest(TestCase):
    def expect(self, encoded, decoded):
        data = deHexStr(encoded)
        assert read_encoded_value(BytesIO(data)) == decoded

    def test_0x00(self):
        illegal = deHexStr("00")
        with pytest.raises(EOFError):
            read_encoded_value(BytesIO(illegal))

    def test_0x19(self):
        illegal = deHexStr("19")
        with pytest.raises(ValueError):
            read_encoded_value(BytesIO(illegal))

    def test_0x20(self):
        self.expect("20", -107)

    def test_0x8b(self):
        self.expect("8b", 0)

    def test_0xf6(self):
        self.expect("f6", 107)

    def test_0xf700(self):
        self.expect("f700", 108)

    def test_0xf701(self):
        self.expect("f701", 109)

    def test_0xf7ff(self):
        self.expect("f7ff", 363)

    def test_0xf800(self):
        self.expect("f800", 364)

    def test_0xf801(self):
        self.expect("f801", 365)

    def test_0xfa00(self):
        self.expect("fa00", 876)

    def test_0xfaff(self):
        self.expect("faff", 1131)

    def test_0xfb00(self):
        self.expect("fb00", -108)

    def test_0xfb01(self):
        self.expect("fb01", -109)

    def test_0xfe00(self):
        self.expect("fe00", -876)

    def test_0xfeff(self):
        self.expect("feff", -1131)

    def test_0xff00000000(self):
        self.expect("ff00000000", 0)

    def test_0xff00001000(self):
        self.expect("ff00001000", 4096)

    def test_0xffffffffff(self):
        self.expect("ffffffffff", -1)

    def test_0xffffffefff(self):
        self.expect("ffffffefff", -4097)


class EncodedValueListParserTest(TestCase):
    def expect(self, encoded, decoded):
        data = deHexStr(encoded)
        assert EncodedValueListParser.parse(BytesIO(data), len(data)) == decoded

    def test_links_1(self):
        self.expect("8c8d898b", [1, 2, -2, 0])


class GlyphParserTest(TestCase):
    def test_glyph_1(self):
        data = b'\x01\t\x07\x01\x01\x91dagger\x08\x8c\xf70\xa5\x00\xf7}\xa5\x01\x8b\xf7t\x01\xa5\xf7W\x01\xac\x8b\x01\xa5\xfbW\x01\x8b\xfbt\x01q\xfbv\x01j\x8b\x00\xfbg\xf9h\x01\xe2\x8b\x01\xf1o\x01\x8bo\x01%o\x014\x8b\x00\xf7M\xf7q\x01\x8b\xe2\x01\xe0\x8b\x01\x8b4\x01q\xfb"\x01j\x8b\x00\xc2X\x01\x8b\xa7\x01\xf1\xa7\x01\xe2\x8b\x01\x8b7\x014\x8b\x02\xf8\xbb\x8b\x03\x8e\xf9\x80w\xfbGv\xf8L\xdf\x8c\xf7}\xe0\x8b\x04\x8b\x8b\n\xa3\x90\x01\x9a\x8e\x02\x92\x8c\x06\x93\x98\x8a\x04\x93\xa1\x8a\x8a\x04\x98\xa4\x8a\x8a\x8b\x8b\x8b\x0f'
        print(hexStr(data))
        result = GlyphParser.parse(BytesIO(data), len(data))
