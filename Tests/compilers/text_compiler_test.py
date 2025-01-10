from fontTools.misc.textTools import deHexStr, hexStr
from unittest import TestCase

from vfbLib.compilers.text import StringCompiler
from vfbLib.parsers.text import StringParser


expected_regular = hexStr(deHexStr("52 65 67 75 6C 61 72"))
expected_space = hexStr(deHexStr("57 74 30 20 57 64 31 20"))
expected_nospace = hexStr(deHexStr("57 74 30 20 57 64 31"))


class StringCompilerTest(TestCase):
    def test_regular(self):
        result = StringCompiler().compile_hex("Regular")
        assert result == expected_regular

    def test_space(self):
        result = StringCompiler().compile_hex("Wt0 Wd1 ")  # Trailing space is compiled
        assert result == expected_space

    def test_space_roundtrip(self):
        dec = StringParser().parse_hex(expected_space)
        assert dec == "Wt0 Wd1"  # Trailing space gets stripped
        cde = StringCompiler().compile_hex(dec)
        assert cde == expected_nospace
