from fontTools.misc.textTools import hexStr
from unittest import TestCase
from vfbLib.compilers.header import VfbHeaderCompiler

header_504 = {
    "header0": 26,
    "filetype": "WLF10",
    "header1": 3,
    "header2": 44,
    "reserved": "00000000000000000000000000000000000000000000000000000000000000000000",
    "header3": 1,
    "header4": 0,
    "header5": 4,
    "header6": 0,
    "header7": 10,
    "header8": 11,
    "header9": {1: 0},
    "header10": {2: 83886081},
    "header11": {3: 0},
    "header12": 0,
    "header13": 262,
    "header14": 0,
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
    "header2": 44,
    "reserved": "00000000000000000000000000000000000000000000000000000000000000000000",
    "header3": 1,
    "header4": 0,
    "header5": 4,
    "header6": 0,
    "header7": 10,
    "header8": 11,
    "header9": {1: 1},
    "header10": {2: 84017792},
    "header11": {3: 0},
    "header12": 0,
    "header13": 262,
    "header14": 0,
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
