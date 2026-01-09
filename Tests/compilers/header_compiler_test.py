from unittest import TestCase

from fontTools.misc.textTools import hexStr

from vfbLib.compilers.header import VfbHeaderCompiler
from vfbLib.typing import VfbHeaderDict

header: VfbHeaderDict = {
    "signature": 1179408154,
    "app_version": 49,
    "file_version": 48,
    "version_major": 3,
    "version_minor": 0,
}

header_hex = (
    "1a574c46313003002c"
    "000000000000000000"
    "000000000000000000"
    "000000000000000000"
    "000000000000000000"
    "00"
)


class VfbHeaderCompilerTest(TestCase):
    def test_compilation(self):
        b = VfbHeaderCompiler().compile(header)
        assert hexStr(b) == header_hex
