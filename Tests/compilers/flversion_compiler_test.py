from unittest import TestCase

from fontTools.misc.textTools import hexStr

from vfbLib.compilers.flversion import FLVersionCompiler

info_504 = {
    "platform": "macos",
    "version": [5, 0, 4, 128],
    "owner": 4616,
}

info_522 = {
    "platform": "macos",
    "version": [5, 2, 2, 128],
    "owner": 4616,
}

info_504_hex = "018c02ff0500048003ff0000120800"

info_522_hex = "018c02ff0502028003ff0000120800"


class VfbHeaderCompilerTest(TestCase):
    def test_compilation_504(self):
        b = FLVersionCompiler().compile(info_504)
        assert hexStr(b) == info_504_hex

    def test_compilation_522(self):
        b = FLVersionCompiler().compile(info_522)
        assert hexStr(b) == info_522_hex
