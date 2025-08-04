from unittest import TestCase

from fontTools.misc.textTools import hexStr

from vfbLib.compilers.header import VfbHeaderCompiler

header_504 = {
    "header0": 26,
    "filetype": "WLF10",
    "header1": 3,
    "chunk1": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        4,
        0,
        0,
        0,
        10,
        0,
    ],
    "creator": {1: 0, 2: [5, 0, 0, 1], 3: 0},
    "end0": 6,
    "end1": 1,
    "end2": 0,
}

header_504_hex = (
    "1a574c46313003002c"
    "000000000000000000"
    "000000000000000000"
    "000000000000000000"
    "000000000000000001"
    "000000040000000a00"
    "0b00018b02ff050000"
    "01038b0006010000"
)

header_522 = {
    "header0": 26,
    "filetype": "WLF10",
    "header1": 3,
    "chunk1": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        4,
        0,
        0,
        0,
        10,
        0,
    ],
    "creator": {1: 1, 2: [5, 2, 2, 128], 3: 0},
    "end0": 6,
    "end1": 1,
    "end2": 0,
}

header_522_hex = (
    "1a574c46313003002c"
    "000000000000000000"
    "000000000000000000"
    "000000000000000000"
    "000000000000000001"
    "000000040000000a00"
    "0b00018c02ff050202"
    "80038b0006010000"
)


class VfbHeaderCompilerTest(TestCase):
    def test_compilation_504(self):
        b = VfbHeaderCompiler().compile(header_504)
        assert hexStr(b) == header_504_hex

    def test_compilation_522(self):
        b = VfbHeaderCompiler().compile(header_522)
        assert hexStr(b) == header_522_hex
