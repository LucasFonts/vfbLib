from fontTools.misc.textTools import deHexStr, hexStr
from io import BytesIO
from unittest import TestCase

from vfbLib.compilers.text import StringCompiler
from vfbLib.parsers.text import StringParser


expected_regular = deHexStr("52 65 67 75 6C 61 72")
expected_space = deHexStr("57 74 30 20 57 64 31 20")


class StringCompilerTest(TestCase):
    def test_regular(self):
        data = StringCompiler().compile("Regular")
        assert hexStr(data) == hexStr(expected_regular)

    def test_space(self):
        data = StringCompiler().compile("Wt0 Wd1 ")
        assert hexStr(data) == hexStr(expected_space)

    def test_space_roundtrip(self):
        dec = StringParser().parse(BytesIO(expected_space), len(expected_space))
        assert dec == "Wt0 Wd1 "
        cde = StringCompiler().compile(dec)
        assert hexStr(cde) == hexStr(expected_space)
