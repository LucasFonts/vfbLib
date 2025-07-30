from io import BytesIO
from unittest import TestCase

from fontTools.misc.textTools import deHexStr, hexStr

from vfbLib.compilers.glyph import (
    GlobalMaskCompiler,
    GlyphCompiler,
    LinksCompiler,
    MaskCompiler,
)
from vfbLib.parsers.glyph import GlyphParser

composite_2_masters_binary = """
01 09 07 01
01    94 41 64 69 65 72 65 73 69 73
08    8D 8B 8B
02    F8F1 8B F915 8B
03    8B 8B 8B
05    8D
      91
      8B 8B
      000000000000F03F
      000000000000F03F
      8B 8B
      000000000000F03F
      000000000000F03F
      FF00000715
      C4 8B
      000000000000F03F
      000000000000F03F
      D6 8B
      000000000000F03F
      000000000000F03F
06    8C
      FA2B FB0B 2C
0F
"""

composite_2_masters_json = {
    "components": [
        {
            "gid": 6,
            "offsetX": [0, 0],
            "offsetY": [0, 0],
            "scaleX": [1.0, 1.0],
            "scaleY": [1.0, 1.0],
        },
        {
            "gid": 1813,
            "offsetX": [57, 75],
            "offsetY": [0, 0],
            "scaleX": [1.0, 1.0],
            "scaleY": [1.0, 1.0],
        },
    ],
    "kerning": {919: [-119, -95]},
    "metrics": [(605, 0), (641, 0)],
    "name": "Adieresis",
    "nodes": [],
    "num_masters": 2,
}

components_2_masters_binary = deHexStr(
    """
05    8D
      91
      8B 8B
      000000000000F03F
      000000000000F03F
      8B 8B
      000000000000F03F
      000000000000F03F
      FF00000715
      C4 8B
      000000000000F03F
      000000000000F03F
      D6 8B
      000000000000F03F
      000000000000F03F
"""
)


components_2_masters_json = {
    "components": [
        {
            "gid": 6,
            "offsetX": [0, 0],
            "offsetY": [0, 0],
            "scaleX": [1.0, 1.0],
            "scaleY": [1.0, 1.0],
        },
        {
            "gid": 1813,
            "offsetX": [57, 75],
            "offsetY": [0, 0],
            "scaleX": [1.0, 1.0],
            "scaleY": [1.0, 1.0],
        },
    ]
}

empty_glyph_binary = """
01 09 07 01
01    90
      2E 6E 75 6C 6C
08    8D
      8B 8B
02    8B 8B 8B 8B
03    8B 8B 8B
0F
"""

empty_glyph_json = {
    "name": ".null",
    "num_masters": 2,
    "nodes": [],
    "metrics": [(0, 0), (0, 0)],
}

long_binary = """
01 09 07 01
01    98
      4C 61 74 69 6E 43 61 70 69 74 61 6C 73
08    8D
      FF00000564
      F71E
      00 F7 A6 FB38 F7AF FB3D
      04 79 82 79 83
      04 5C 7F 5E 82
      01 708B708B04678B578B0454A648A70467BE63C00479D47BD4018BBA8BB8048BB88BBC049CD9A3DB04B1C4B9C304C6ACCFA901B48BB88B04A08BA28B04B383B584019D84998601816A7229047A93828E046793768F01798B808B046D8B7C8B04606F758004705B7C72047F4C8463018B678B6F048B3A8B5304C231A55B01C48BA88B04A18B998B04B095A28F019A93969000F7B85DF7A521016DF17EC901FB2A8B2A8B016D257F4D01648BFB0D8B01F70DF826E7F82601BB8BF7538B01F70EFC26E7FC2600FB18F7C5FB4DF79504869B89990485A787A701879B899C018B8B8A8B04887D8A7A04846E876F01867C887D0158FB42762401F7188BC68B00F732FB19F74FFB2E018BF8268BF825049D8CA58D04B28BD48D019D8BB38B04CA8BDB8B04C64DD546018B568B45048B6E8B6704795C7354046A696065045B795178016C8B698B04848B898B047C8B868B01848C898B018BFB358BFB0A008BF7558BF76704928A8D8A049B8A918A01948B8F8B04B88B998B04B5BC99A6018BB68BA3048BB68BA20461B97EA9015E8B7B8B04858B898B04798B878B01838A868B00FD23F722FDA7F75C018BF8268BF82601B18BF7118B018BFC068BFBC201F7108BE18B018B6B8B2700F7B18BF7958B016DF17EC901FB2A8B2A8B016D257F4D01648BFB0D8B01F70DF826E7F82601BB8BF7538B01F70EFC26E7FC2600FB18F7C5FB4DF79504869B89990485A787A701879B899C018B8B8A8B04887D8A7A04846E876F01867C887D0158FB42762401F7188BC68B00F764F781F7D5F729018BFC068BFBC301658BFB118B018BF8068BF7C301268B4A8B018BAB8BEE01F7848BF7948B018B6B8B2800F7AAFC06F769FBC301FB19F7AF55F75304839C869F047CAE83B40183A189A2018A8B898B048C668D68048DFB0A8D55018B388B6E018BFB0B8BFB3101668BFB028B018BF8268BF82601C08BF74B8B01F718FBB0B5FB2804937D9177049B63935C0192798D7A018C8B8D8B048AA18A9D048AC989AD048AD08AAA048BD08BA5018BA98B94018BF38BF70601B08BF7018B018BFC268BFC2602FF0000048A8BFF000004E78B038B8B8B0F"""

glyph_guides_binary = """
04    8C
      F93A 8B
      8C
      F715 8B
"""

glyph_guides_json = {
    "guides": {
        "h": [[{"pos": 678, "angle": 0.0}]],
        "v": [[{"pos": 129, "angle": 0.0}]],
    }
}

angled_glyph_guides_binary = "04 8C F8C7 F849 8C F7E5 FF00000943"

angled_glyph_guides_json = {
    "guides": {
        "h": [[{"pos": 563, "angle": 2.502233544934958}]],
        "v": [[{"pos": 337, "angle": 13.33852189395167}]],
    }
}


psglyph_1master = """
01 09 07 01
01    8C 64
08    8C F87E B2
      00 F7FC F92C
      13 8F FB02 89 D5 8E 66
      13 78 FBAB 9B F735 80 3B
      13 87 FBA8 86 F716 8D 4B
      03 99 FB55 82 E2 87 5B
      01 F715 68
      03 8C 8E 8B 89 8B 8C
      03 FB0A 97 DA 84 64 8F
      01 63 8B
      01 F706 9F
      13 8F 7E 86 9C 8E 7F
      03 8B 8F 8E 80 89 93
      11 86 B0
      13 88 CE 8B 5E 8C A2
      03 89 F76D 89 FB15 8A CB
      03 9C F835 88 FB7E 92 F708
      00 6C FB9C
      13 40 F738 F702 26 51 CF
      13 28 CA AB 77 7E 99
      13 FB B5 28 F73C F71F FB0B 62
      13 3D FBA6 8E F70F 86 4A
      13 BD FB6D 5D F395 4F
      13 F78D 34 FB3D 81 F67D
      03 F76F F73E 2B FB0E D8 C5
      01 2D E6
      03 36 37 D5 BA 62 6E
      33 5E 78 93 8C 87 8A
      03 55 8D AC 89 7B 8C
      13 98 F7C5 34 FB8A 88 F769
      33 F727 AD 65 91 9F 85
      03 A4 89 84 8D 95 89
      13 75 92 98 87 85 8D
      13 B1 70 5D A9 A8 78
      13 A5 7A 86 8F 93 84
      13 79 9B 96 83 85 8F
      03 8E 87 80 95 94 84
      13 A4 6E 7D 9E 93 82
      03 9C 69 84 9C 90 83
      03 8F 8D 89 77 96 B0
02    F8B4 8B
03    8F
      7F C3 F818 C3 F92A 53 85 C2
      8D C1 EB F802 E5
      8B
0F
"""

psglyph_1master_nodes = deHexStr(
    """
08    8C F87E B2
      00 F7FC F92C
      13 8F FB02 89 D5 8E 66
      13 78 FBAB 9B F735 80 3B
      13 87 FBA8 86 F716 8D 4B
      03 99 FB55 82 E2 87 5B
      01 F715 68
      03 8C 8E 8B 89 8B 8C
      03 FB0A 97 DA 84 64 8F
      01 63 8B
      01 F706 9F
      13 8F 7E 86 9C 8E 7F
      03 8B 8F 8E 80 89 93
      11 86 B0
      13 88 CE 8B 5E 8C A2
      03 89 F76D 89 FB15 8A CB
      03 9C F835 88 FB7E 92 F708
      00 6C FB9C
      13 40 F738 F702 26 51 CF
      13 28 CA AB 77 7E 99
      13 FB B5 28 F73C F71F FB0B 62
      13 3D FBA6 8E F70F 86 4A
      13 BD FB6D 5D F395 4F
      13 F78D 34 FB3D 81 F67D
      03 F76F F73E 2B FB0E D8 C5
      01 2D E6
      03 36 37 D5 BA 62 6E
      33 5E 78 93 8C 87 8A
      03 55 8D AC 89 7B 8C
      13 98 F7C5 34 FB8A 88 F769
      33 F727 AD 65 91 9F 85
      03 A4 89 84 8D 95 89
      13 75 92 98 87 85 8D
      13 B1 70 5D A9 A8 78
      13 A5 7A 86 8F 93 84
      13 79 9B 96 83 85 8F
      03 8E 87 80 95 94 84
      13 A4 6E 7D 9E 93 82
      03 9C 69 84 9C 90 83
      03 8F 8D 89 77 96 B0
"""
)

# fmt: off
psglyph_1master_expected = {
    "name": "d",
    "num_masters": 1,
    "nodes": [
        {"type": "move",  "flags": 0, "points": [[(360, 664)]]},
        {"type": "curve", "flags": 1, "points": [[(364, 554), (362, 628), (365, 591)]]},
        {"type": "curve", "flags": 1, "points": [[(346, 312), (362, 473), (351, 393)]]},
        {"type": "curve", "flags": 1, "points": [[(347, 117), (342, 247), (344, 183)]]},
        {"type": "curve", "flags": 0, "points": [[(358, -10), (349,  77), (345,  29)]]},
        {"type": "line",  "flags": 0, "points": [[(474,  -6)]]},
        {"type": "curve", "flags": 0, "points": [[(475,  -3), (475,  -5), (475,  -4)]]},
        {"type": "curve", "flags": 0, "points": [[(357,   8), (436,   1), (397,   5)]]},
        {"type": "line",  "flags": 0, "points": [[(357,   5)]]},
        {"type": "line",  "flags": 0, "points": [[(471,  25)]]},
        {"type": "curve", "flags": 1, "points": [[(475,  12), (470,  29), (473,  17)]]},
        {"type": "curve", "flags": 0, "points": [[(473,  21), (476,  10), (474,  18)]]},
        {"type": "line",  "flags": 1, "points": [[(469,  55)]]},
        {"type": "curve", "flags": 1, "points": [[(466, 122), (466,  77), (467, 100)]]},
        {"type": "curve", "flags": 0, "points": [[(465, 317), (463, 188), (462, 252)]]},
        {"type": "curve", "flags": 0, "points": [[(479, 669), (476, 435), (483, 551)]]},
        {"type": "move",  "flags": 0, "points": [[(452, 287)]]},
        {"type": "curve", "flags": 1, "points": [[(377, 451), (487, 350), (429, 418)]]},
        {"type": "curve", "flags": 1, "points": [[(330, 481), (362, 461), (349, 475)]]},
        {"type": "curve", "flags": 1, "points": [[( 60, 376), (228, 515), (109, 474)]]},
        {"type": "curve", "flags": 1, "points": [[( 31, 200), ( 34, 323), ( 29, 258)]]},
        {"type": "curve", "flags": 1, "points": [[( 79,  41), ( 33, 145), ( 43,  85)]]},
        {"type": "curve", "flags": 1, "points": [[(292,  -2), (123, -12), (230, -26)]]},
        {"type": "curve", "flags": 0, "points": [[(449, 144), (353,  22), (430,  80)]]},
        {"type": "line",  "flags": 0, "points": [[(336, 171)]]},
        {"type": "curve", "flags": 0, "points": [[(251,  87), (325, 134), (284, 105)]]},
        {"type": "curve", "flags": 3, "points": [[(239,  86), (247,  87), (243,  86)]]},
        {"type": "curve", "flags": 0, "points": [[(189,  88), (222,  86), (206,  87)]]},
        {"type": "curve", "flags": 1, "points": [[(219, 392), (132, 146), (129, 359)]]},
        {"type": "curve", "flags": 3, "points": [[(276, 393), (238, 399), (258, 393)]]},
        {"type": "curve", "flags": 0, "points": [[(283, 391), (276, 393), (286, 391)]]},
        {"type": "curve", "flags": 1, "points": [[(264, 398), (277, 394), (271, 396)]]},
        {"type": "curve", "flags": 1, "points": [[(309, 369), (263, 399), (292, 380)]]},
        {"type": "curve", "flags": 1, "points": [[(318, 363), (313, 367), (321, 360)]]},
        {"type": "curve", "flags": 1, "points": [[(303, 376), (314, 368), (308, 372)]]},
        {"type": "curve", "flags": 0, "points": [[(311, 368), (300, 378), (309, 371)]]},
        {"type": "curve", "flags": 1, "points": [[(334, 342), (320, 361), (328, 352)]]},
        {"type": "curve", "flags": 0, "points": [[(345, 318), (338, 335), (343, 327)]]},
        {"type": "curve", "flags": 0, "points": [[(347, 329), (345, 309), (356, 346)]]},
        #          39                             + 39 + 39  +  32 + 32  +  32 + 32 = 245
    ],
    "metrics": [(544, 0)],
    "hints": {
        "v": [[{"pos": 54, "width": 96}], [{"pos": 366, "width": 90}]],
        "h": [
            [{"pos": -12, "width": 56}],
            [{"pos": 388, "width": 56}],
            [{"pos": 662, "width": -56}],
            [{"pos": -6, "width": 55}],
        ],
    },
}
# fmt: on

ttglyph_2_masters_binary = """
01 09 07 01
01    8C 6F
08    8D F784 A3
      00 F87F F790 F8B1 F79D
      04 8B FB09 8B FB10
      04 FB10 FB23 FB27 FB2D
      01 21 8B FB0F 8B
      04 25 8B FB0D 8B
      04 FB04 F717 FB13 F710
      01 8B F70E 8B F70C
      04 8B F709 8B F710
      04 F710 F723 F727 F72D
      01 F58B F70F 8B
      04 F18B F70D 8B
      04 F704 FB17 F713 FB10
      00 54 FB11 FB51 FB1D
      04 8B F0 8B BF
      04 33 F704 68 C0
      01 3D 8B 69 8B
      04 3C 8B 68 8B
      04 32 FB04 67 54
      01 8B 25 8B 5A
      04 8B 27 8B 57
      04 E3 FB04 AE 57
      01 D9 8B AD 8B
      04 DA 8B AE 8B
      04 E4 F703 AF C1
02    F8 AE 8B F8C8 8B
03    8B 8B 8B
06    93
      F9A2 82 7E
      F9A8 8A 84
      F9B7 7B 6F
      F9BA 87 85
      FF000004F3 70 77
      FF00000505 59 77
      FF00000506 68 7E
      FF0000053C 7A 8A
0A    B1
      93
      07 91 8B
      03 91 97 89 8A
      03 97 8B 8B 8A
      03 91 9D 8B 8A
      01 94 93
      02 8E 8C
      04 94 9A 8B 8A
      04 8E A0 8B 8A
      8B 8B 8B
0F"""

ttglyph_2_masters_json = {
    "kerning": {
        782: [-9, -13],
        788: [-1, -7],
        803: [-16, -28],
        806: [-4, -6],
        1267: [-27, -20],
        1285: [-50, -20],
        1286: [-35, -13],
        1340: [-17, -1],
    },
    "metrics": [(538, 0), (564, 0)],
    "name": "o",
    "nodes": [
        {"flags": 0, "points": [[(491, 252)], [(541, 265)]], "type": "move"},
        {"flags": 0, "points": [[(491, 135)], [(541, 141)]], "type": "qcurve"},
        {"flags": 0, "points": [[(367, -8)], [(394, -12)]], "type": "qcurve"},
        {"flags": 0, "points": [[(261, -8)], [(271, -12)]], "type": "line"},
        {"flags": 0, "points": [[(159, -8)], [(150, -12)]], "type": "qcurve"},
        {"flags": 0, "points": [[(47, 123)], [(23, 112)]], "type": "qcurve"},
        {"flags": 0, "points": [[(47, 245)], [(23, 232)]], "type": "line"},
        {"flags": 0, "points": [[(47, 362)], [(23, 356)]], "type": "qcurve"},
        {"flags": 0, "points": [[(171, 505)], [(170, 509)]], "type": "qcurve"},
        {"flags": 0, "points": [[(277, 505)], [(293, 509)]], "type": "line"},
        {"flags": 0, "points": [[(379, 505)], [(414, 509)]], "type": "qcurve"},
        {"flags": 0, "points": [[(491, 374)], [(541, 385)]], "type": "qcurve"},
        {"flags": 0, "points": [[(436, 249)], [(352, 248)]], "type": "move"},
        {"flags": 0, "points": [[(436, 350)], [(352, 300)]], "type": "qcurve"},
        {"flags": 0, "points": [[(348, 462)], [(317, 353)]], "type": "qcurve"},
        {"flags": 0, "points": [[(270, 462)], [(283, 353)]], "type": "line"},
        {"flags": 0, "points": [[(191, 462)], [(248, 353)]], "type": "qcurve"},
        {"flags": 0, "points": [[(102, 350)], [(212, 298)]], "type": "qcurve"},
        {"flags": 0, "points": [[(102, 248)], [(212, 249)]], "type": "line"},
        {"flags": 0, "points": [[(102, 148)], [(212, 197)]], "type": "qcurve"},
        {"flags": 0, "points": [[(190, 36)], [(247, 145)]], "type": "qcurve"},
        {"flags": 0, "points": [[(268, 36)], [(281, 145)]], "type": "line"},
        {"flags": 0, "points": [[(347, 36)], [(316, 145)]], "type": "qcurve"},
        {"flags": 0, "points": [[(436, 147)], [(352, 199)]], "type": "qcurve"},
    ],
    "num_masters": 2,
    "tth": [
        {"cmd": "AlignH", "params": {"align": 0, "pt": 6}},
        {
            "cmd": "SingleLinkH",
            "params": {"align": -1, "pt1": 6, "pt2": 12, "stem": -2},
        },
        {"cmd": "SingleLinkH", "params": {"align": -1, "pt1": 12, "pt2": 0, "stem": 0}},
        {"cmd": "SingleLinkH", "params": {"align": -1, "pt1": 6, "pt2": 18, "stem": 0}},
        {"cmd": "AlignTop", "params": {"pt": 9, "zone": 8}},
        {"cmd": "AlignBottom", "params": {"pt": 3, "zone": 1}},
        {"cmd": "SingleLinkV", "params": {"align": -1, "pt1": 9, "pt2": 15, "stem": 0}},
        {"cmd": "SingleLinkV", "params": {"align": -1, "pt1": 3, "pt2": 21, "stem": 0}},
    ],
}

ttinstructions_binary = """
0A    B1
      93
      07 91 8B
      03 91 97 89 8A
      03 97 8B 8B 8A
      03 91 9D 8B 8A
      01 94 93
      02 8E 8C
      04 94 9A 8B 8A
      04 8E A0 8B 8A
      8B 8B 8B
"""

ttinstructions_json = {
    "tth": [
        {"cmd": "AlignH", "params": {"align": 0, "pt": 6}},
        {
            "cmd": "SingleLinkH",
            "params": {"align": -1, "pt1": 6, "pt2": 12, "stem": -2},
        },
        {"cmd": "SingleLinkH", "params": {"align": -1, "pt1": 12, "pt2": 0, "stem": 0}},
        {"cmd": "SingleLinkH", "params": {"align": -1, "pt1": 6, "pt2": 18, "stem": 0}},
        {"cmd": "AlignTop", "params": {"pt": 9, "zone": 8}},
        {"cmd": "AlignBottom", "params": {"pt": 3, "zone": 1}},
        {"cmd": "SingleLinkV", "params": {"align": -1, "pt1": 9, "pt2": 15, "stem": 0}},
        {"cmd": "SingleLinkV", "params": {"align": -1, "pt1": 3, "pt2": 21, "stem": 0}},
    ],
}


class PartCompiler(GlyphCompiler):
    """
    Compile part of the glyph data, by calling the method name passed in compile_method.
    """

    def _compile(self, data, master_count, compile_method):
        self.stream = BytesIO()
        self.master_count = master_count
        getattr(self, compile_method)(data)
        return self.stream.getvalue()


class GlyphCompilerTest(TestCase):
    def test_empty_2masters_roundtrip(self):
        # Decompile
        dec = GlyphParser().parse_hex(empty_glyph_binary, 2)
        assert dec == empty_glyph_json

        # Compile
        compiled = GlyphCompiler().compile_hex(dec, 2)
        # ... and parse again
        cde = GlyphParser().parse_hex(compiled, 2)
        assert dec == cde

    def test_long_roundtrip(self):
        # Decompile
        dec = GlyphParser().parse_hex(long_binary, 2)
        # assert dec == {}

        # Compile
        compiled = GlyphCompiler().compile_hex(dec, 2)
        # print(hexStr(compiled))
        # ... and parse again
        cde = GlyphParser().parse_hex(compiled, 2)
        assert dec == cde

    def test_psglyph_1master_roundtrip(self):
        # Decompile
        dec = GlyphParser().parse_hex(psglyph_1master, 1)
        assert dec == psglyph_1master_expected

        # Compile
        compiled = GlyphCompiler().compile_hex(dec, 1)
        # print(hexStr(compiled))
        # ... and parse again
        cde = GlyphParser().parse_hex(compiled, 1)
        assert dec == cde

    def test_truetype_2_masters_roundtrip(self):
        # Decompile
        dec = GlyphParser().parse_hex(ttglyph_2_masters_binary)
        assert dec == ttglyph_2_masters_json

        # Compile
        compiled = GlyphCompiler().compile_hex(dec, 2)
        # print(hexStr(compiled))
        # ... and parse again
        cde = GlyphParser().parse_hex(compiled, 2)
        assert dec == cde

    def test_composite_2_masters_roundtrip(self):
        # Decompile
        dec = GlyphParser().parse_hex(composite_2_masters_binary, 2)
        assert dec == composite_2_masters_json

        # Compile
        compiled = GlyphCompiler().compile_hex(dec, 2)
        # ... and parse again
        cde = GlyphParser().parse_hex(compiled, 2)
        assert dec == cde

    def test_components_2_masters(self):
        data = PartCompiler()._compile(
            components_2_masters_json, 2, "_compile_components"
        )
        assert hexStr(data) == hexStr(components_2_masters_binary)

    def test_guides_1_master(self):
        data = PartCompiler()._compile(glyph_guides_json, 1, "_compile_guides")
        assert hexStr(data) == hexStr(deHexStr(glyph_guides_binary))

    def test_guides_angled_1_master(self):
        data = PartCompiler()._compile(angled_glyph_guides_json, 1, "_compile_guides")
        assert hexStr(data) == hexStr(deHexStr(angled_glyph_guides_binary))

    def test_hints_1(self):
        data = PartCompiler()._compile(psglyph_1master_expected, 1, "_compile_hints")
        assert hexStr(data) == hexStr(
            deHexStr("03    8F  7F C3 F818 C3 F92A 53 85 C2  8D C1 EB F802 E5  8B")
        )

    def test_metrics_1(self):
        data = PartCompiler()._compile(psglyph_1master_expected, 1, "_compile_metrics")
        assert hexStr(data) == "02f8b48b"

    def test_name_1(self):
        data = PartCompiler()._compile({"name": "d"}, 1, "_compile_glyph_name")
        assert hexStr(data) == hexStr(deHexStr("01 8C 64"))

    def test_name_2(self):
        data = PartCompiler()._compile({"name": "at"}, 1, "_compile_glyph_name")
        assert hexStr(data) == hexStr(deHexStr("01 8D 61 74"))

    def test_outlines_1_master(self):
        data = PartCompiler()._compile(psglyph_1master_expected, 1, "compile_outlines")
        assert hexStr(data) == hexStr(psglyph_1master_nodes)
        assert len(data) == len(psglyph_1master_nodes)  # 285

    def test_instructions_2_masters(self):
        data = PartCompiler()._compile(ttinstructions_json, 2, "_compile_instructions")
        assert hexStr(data) == hexStr(deHexStr(ttinstructions_binary))
        # assert len(data) == len(psglyph_1master_nodes)  # 285

    def test_imported_binary(self):
        data = PartCompiler()._compile(imported_glyph_raw, 1, "_compile_binary")
        assert hexStr(data) == hexStr(deHexStr(imported_glyph_bin))

    def test_imported_binary_no_nodes(self):
        result = GlyphCompiler().compile_hex(glyph_roundtripped_raw)
        assert result == glyph_roundtripped_bin


raw_links = {"x": [[7, 2], [9, 16]], "y": [[6, 3], [10, 15], [0, -1], [17, 8]]}
bin_links = (
    "8f"  # 4: y
    "918e"
    "959a"
    "8b8a"
    "9c93"
    "8d"  # 2: x
    "928d"
    "949b"
)


class LinksCompilerTest(TestCase):
    def test(self) -> None:
        result = LinksCompiler().compile_hex(raw_links)
        assert result == bin_links


raw_mask_mm = {
    "num": 2,
    "reserved0": 100000000,
    "reserved1": 0,
    "num_masters": 2,
    "nodes": [
        {"type": "move", "flags": 0, "points": [[[419, 0]], [[459, 0]]]},
        {
            "type": "curve",
            "flags": 1,
            "points": [
                [[417, 158], [418, 46], [417, 105]],
                [[456, 126], [456, 40], [456, 87]],
            ],
        },
        {"type": "line", "flags": 1, "points": [[[417, 329]], [[456, 327]]]},
        {
            "type": "curve",
            "flags": 3,
            "points": [
                [[247, 505], [417, 433], [374, 505]],
                [[251, 507], [456, 444], [407, 507]],
            ],
        },
        {
            "type": "curve",
            "flags": 0,
            "points": [
                [[80, 460], [189, 505], [130, 488]],
                [[66, 468], [191, 507], [122, 493]],
            ],
        },
        {"type": "line", "flags": 0, "points": [[[97, 419]], [[95, 367]]]},
        {
            "type": "curve",
            "flags": 3,
            "points": [
                [[241, 462], [143, 447], [195, 462]],
                [[235, 403], [141, 390], [189, 403]],
            ],
        },
        {
            "type": "curve",
            "flags": 1,
            "points": [
                [[364, 321], [335, 462], [364, 413]],
                [[323, 326], [299, 403], [323, 377]],
            ],
        },
        {"type": "line", "flags": 0, "points": [[[364, 287]], [[323, 308]]]},
        {"type": "line", "flags": 0, "points": [[[345, 287]], [[315, 308]]]},
        {
            "type": "curve",
            "flags": 3,
            "points": [
                [[55, 125], [149, 287], [55, 225]],
                [[33, 138], [139, 308], [33, 252]],
            ],
        },
        {
            "type": "curve",
            "flags": 3,
            "points": [
                [[202, -8], [55, 46], [114, -8]],
                [[192, -10], [33, 51], [89, -10]],
            ],
        },
        {
            "type": "curve",
            "flags": 0,
            "points": [
                [[369, 102], [285, -8], [344, 39]],
                [[337, 72], [258, -10], [311, 20]],
            ],
        },
        {"type": "line", "flags": 0, "points": [[[370, 102]], [[338, 72]]]},
        {
            "type": "curve",
            "flags": 0,
            "points": [
                [[364, 0], [365, 72], [364, 42]],
                [[333, 0], [334, 48], [333, 22]],
            ],
        },
        {"type": "move", "flags": 1, "points": [[[364, 229]], [[323, 211]]]},
        {
            "type": "curve",
            "flags": 3,
            "points": [
                [[206, 35], [364, 121], [301, 35]],
                [[219, 95], [323, 149], [281, 95]],
            ],
        },
        {
            "type": "curve",
            "flags": 3,
            "points": [
                [[110, 129], [146, 35], [110, 76]],
                [[166, 147], [187, 95], [166, 116]],
            ],
        },
        {
            "type": "curve",
            "flags": 0,
            "points": [
                [[343, 244], [110, 197], [162, 244]],
                [[313, 219], [166, 189], [199, 219]],
            ],
        },
        {"type": "line", "flags": 0, "points": [[[364, 244]], [[323, 219]]]},
    ],
}

bin_mask_mm = (
    "8d"  # 2
    "ff05f5e1008b8df81c9f00f8378bf85f8b1389f73288f7128cfb048b358ac68bba118bf7748bf78433fb3ef744fb61f748f73e43f7614c60d35aca03fbba5efbe964f701b8f711b2507a467d016a4670fb1233f724b6f720af297c2d7ebf9abb9813f73dfb21f71a3e6ef72173d8a85aa371018bfb128b4601788b838b33fbb6fb36fbaefb3ee9f736f5f73e2d4d215333f727fb7df733fb9afb27c1fb33c8c655c34e03f793f702f78cdd37fb023c39c6bac0a901a5caa6bf03852586438cd38cbb8a6d8a71108bf74f81f75133fb32fb5623fb08f732e1f3c14c35615533fb53e9fb07bfaf2da05767b476a003f77df73cf727f2fb7d5cfb276dbfbaaca901f75e8bf7108b"
)

raw_mask_1m = {
    "num": 1,
    "reserved0": 100000000,
    "num_masters": 1,
    "nodes": [
        {"type": "move", "flags": 0, "points": [[[32, 0]]]},
        {"type": "line", "flags": 0, "points": [[[424, 0]]]},
        {"type": "line", "flags": 0, "points": [[[424, 780]]]},
        {"type": "line", "flags": 0, "points": [[[32, 780]]]},
        {"type": "move", "flags": 0, "points": [[[81, 50]]]},
        {"type": "line", "flags": 0, "points": [[[81, 730]]]},
        {"type": "line", "flags": 0, "points": [[[376, 730]]]},
        {"type": "line", "flags": 0, "points": [[[376, 50]]]},
    ],
}

bin_mask_1m = (
    "8c"  # 1
    "ff05f5e100"  # 100000000
    "8c"  # 1
    "bb"  # 48
    "93"  # 8
    "00ab8b"  # move: 32 0
    "01f81c8b"  # line: 392 0
    "018bf9a0"  # line: 0 780
    "01fc1c8b"  # line: -392 0
    "00bcfd6e"  # move: 49 -730
    "018bf93c"  # line: 0 680
    "01f7bb8b"  # line: 295 0
    "018bfd3c"  # line: 0 -680
)


class MaskCompilerTest(TestCase):
    def test_1m(self) -> None:
        result = MaskCompiler().compile_hex(raw_mask_1m)
        assert result == bin_mask_1m

    def test_mm(self) -> None:
        result = MaskCompiler().compile_hex(raw_mask_mm)
        assert result == bin_mask_mm


global_mask_raw = {
    "num_masters": 1,
    "nodes": [
        {"type": "move", "flags": 0, "points": [[[400, 74]]]},
        {"type": "line", "flags": 0, "points": [[[664, 262]]]},
        {"type": "curve", "flags": 0, "points": [[[324, 503], [529, 413], [512, 591]]]},
    ],
}

global_mask_bin = "8ca58e00f824d501f79cf75003fbe8f785f761317af746"


class GlobalMaskCompilerTest(TestCase):
    def test_1m(self) -> None:
        result = GlobalMaskCompiler().compile_hex(global_mask_raw)
        assert result == global_mask_bin


imported_glyph_raw = {
    "imported": {
        "width": 617,
        "lsb": 19,
        "unknown1": 0,
        "unknown2": 0,
        "unknown3": 1,
        "bbox": [19, -20, 596, 507],
        "num_contours": 2,
        "endpoints": [44, 64],
        "nodes": [
            {"flags": 23, "on": 1, "point": [168, -6]},
            {"flags": 34, "on": 0, "point": [94, -6]},
            {"flags": 38, "on": 0, "point": [19, 112]},
            {"flags": 55, "on": 1, "point": [36, 232]},
            {"flags": 62, "on": 0, "point": [45, 295]},
            {"flags": 62, "on": 0, "point": [98, 396]},
            {"flags": 62, "on": 0, "point": [174, 468]},
            {"flags": 54, "on": 0, "point": [268, 507]},
            {"flags": 51, "on": 1, "point": [319, 507]},
            {"flags": 50, "on": 0, "point": [366, 507]},
            {"flags": 22, "on": 0, "point": [430, 485]},
            {"flags": 23, "on": 1, "point": [450, 470]},
            {"flags": 30, "on": 0, "point": [456, 465]},
            {"flags": 22, "on": 0, "point": [464, 456]},
            {"flags": 23, "on": 1, "point": [467, 451]},
            {"flags": 54, "on": 0, "point": [479, 454]},
            {"flags": 30, "on": 0, "point": [504, 448]},
            {"flags": 30, "on": 0, "point": [523, 432]},
            {"flags": 22, "on": 0, "point": [533, 406]},
            {"flags": 7, "on": 1, "point": [531, 388]},
            {"flags": 14, "on": 0, "point": [521, 310]},
            {"flags": 6, "on": 0, "point": [512, 204]},
            {"flags": 21, "on": 1, "point": [512, 169]},
            {"flags": 20, "on": 0, "point": [512, 141]},
            {"flags": 30, "on": 0, "point": [520, 105]},
            {"flags": 30, "on": 0, "point": [533, 82]},
            {"flags": 22, "on": 0, "point": [549, 69]},
            {"flags": 23, "on": 1, "point": [557, 65]},
            {"flags": 30, "on": 0, "point": [580, 51]},
            {"flags": 22, "on": 0, "point": [596, 22]},
            {"flags": 14, "on": 0, "point": [589, -4]},
            {"flags": 6, "on": 0, "point": [564, -20]},
            {"flags": 35, "on": 1, "point": [546, -20]},
            {"flags": 34, "on": 0, "point": [508, -20]},
            {"flags": 38, "on": 0, "point": [442, 19]},
            {"flags": 39, "on": 1, "point": [428, 67]},
            {"flags": 46, "on": 0, "point": [420, 91]},
            {"flags": 38, "on": 0, "point": [417, 152]},
            {"flags": 55, "on": 1, "point": [422, 192]},
            {"flags": 6, "on": 0, "point": [400, 146]},
            {"flags": 7, "on": 1, "point": [377, 115]},
            {"flags": 14, "on": 0, "point": [360, 92]},
            {"flags": 14, "on": 0, "point": [315, 48]},
            {"flags": 14, "on": 0, "point": [263, 14]},
            {"flags": 6, "on": 0, "point": [202, -6]},
            {"flags": 55, "on": 1, "point": [328, 189]},
            {"flags": 62, "on": 0, "point": [356, 227]},
            {"flags": 54, "on": 0, "point": [408, 330]},
            {"flags": 55, "on": 1, "point": [425, 395]},
            {"flags": 46, "on": 0, "point": [421, 396]},
            {"flags": 38, "on": 0, "point": [414, 398]},
            {"flags": 39, "on": 1, "point": [410, 400]},
            {"flags": 46, "on": 0, "point": [389, 409]},
            {"flags": 38, "on": 0, "point": [348, 421]},
            {"flags": 35, "on": 1, "point": [327, 421]},
            {"flags": 34, "on": 0, "point": [298, 421]},
            {"flags": 14, "on": 0, "point": [235, 395]},
            {"flags": 14, "on": 0, "point": [181, 341]},
            {"flags": 6, "on": 0, "point": [143, 258]},
            {"flags": 7, "on": 1, "point": [139, 201]},
            {"flags": 6, "on": 0, "point": [134, 142]},
            {"flags": 22, "on": 0, "point": [157, 92]},
            {"flags": 51, "on": 1, "point": [189, 92]},
            {"flags": 50, "on": 0, "point": [213, 92]},
            {"flags": 54, "on": 0, "point": [289, 135]},
        ],
        "instructions": [
            "SVTCA[0]\t/* SetFPVectorToAxis */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "0",
            "RCVT[ ]\t/* ReadCVT */",
            "IF[ ]\t/* If */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "8",
            "MDAP[1]\t/* MoveDirectAbsPt */",
            "ELSE[ ]\t/* Else */",
            "PUSHW[ ]\t/* 2 values pushed */",
            "8",
            "9",
            "MIAP[0]\t/* MoveIndirectAbsPt */",
            "EIF[ ]\t/* EndIf */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "0",
            "RCVT[ ]\t/* ReadCVT */",
            "IF[ ]\t/* If */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "0",
            "MDAP[1]\t/* MoveDirectAbsPt */",
            "ELSE[ ]\t/* Else */",
            "PUSHW[ ]\t/* 2 values pushed */",
            "0",
            "5",
            "MIAP[0]\t/* MoveIndirectAbsPt */",
            "EIF[ ]\t/* EndIf */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "0",
            "RCVT[ ]\t/* ReadCVT */",
            "IF[ ]\t/* If */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "32",
            "MDAP[1]\t/* MoveDirectAbsPt */",
            "ELSE[ ]\t/* Else */",
            "PUSHW[ ]\t/* 2 values pushed */",
            "32",
            "5",
            "MIAP[0]\t/* MoveIndirectAbsPt */",
            "EIF[ ]\t/* EndIf */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "8",
            "SRP0[ ]\t/* SetRefPoint0 */",
            "PUSHW[ ]\t/* 2 values pushed */",
            "54",
            "1",
            "MIRP[10100]\t/* MoveIndirectRelPt */",
            "PUSHW[ ]\t/* 1 value pushed */",
            "0",
            "SRP0[ ]\t/* SetRefPoint0 */",
            "PUSHW[ ]\t/* 2 values pushed */",
            "62",
            "1",
            "MIRP[10100]\t/* MoveIndirectRelPt */",
            "IUP[0]\t/* InterpolateUntPts */",
            "IUP[1]\t/* InterpolateUntPts */",
        ],
        "hdmx": [
            5,
            6,
            7,
            7,
            8,
            9,
            10,
            10,
            11,
            13,
            14,
            16,
            17,
            19,
            20,
            22,
            25,
            28,
            30,
            33,
            35,
            40,
            45,
        ],
    }
}

imported_glyph_bin = (
    "09"  # Imported binary
    "29"  # metrics
    "f8fd"  # 617: width
    "9e"  # 19: lsb
    "8b8b8c"  # unknown
    "9e77f8e8f88f"  # 19, -20, 596, 507: bbox
    "2a"  # Outlines
    "8d"  # 2: num_contours
    "b7cb"  # 44, 64: endpoints
    "cc"  # 65: num_points
    "f73c85"  # 168, -6: coordinates
    "17"  # 23: flags
    "418b"  # -74, 0: coordinates (rel.)
    "22"  # 34: flags
    "40 f70a 26"
    "9c f70c 37"
    "94 ca 3e"
    "c0 f0 3e"
    "d7 d3 3e"
    "e9 b2 36"
    "be 8b 33"
    "ba 8b 32"
    "cb 75 16"
    "9f 7c 17"
    "91 86 1e"
    "93 82 16"
    "8e 86 17"
    "97 8e 36"
    "a4 85 1e"
    "9e 7b 1e"
    "957116897907813d0e8221068b68158b6f1493671e98741e9b7e16938717a27d1e9"
    "b6e1684710e727b06798b23658b2249b2267dbb2783a32e88c82690b337755d06746c077a740e5e5f0"
    "e57690e4e7706f712f75737a7b13ebff2369ccc37878c2e848d26878d2776942e629726768b236e8b"
    "224c710e55550e653806875207865006a25916ab8b33a38b32d7b636"
    "2b"  # Instructions
    "d5"  # 74 bytes follow
    "00b800004558b800082f1bb9000800093e59b800004558b800002f1bb9000000"
    "053e59b800004558b800202f1bb9002000053e59b8000810b900360001f4b800"
    "0010b9003e0001f43031"
    "2c"  # HDMX
    "a2"  # 23 bytes follow
    "0506070708090a0a0b0d0e1011131416191c1e2123282d"  # HDMX data
    "28"  # end of imported binary data
)

glyph_roundtripped_bin = (
    "01090701"
    "01"  # name
    "92"  # 7: name length
    "756e6931453033"  # name
    "08"  # outlines
    "8c"  # 1: masters count
    "8b8b"  # 0 0
    "02"  # metrics
    "f8d98b"
    "05"  # components
    "8d"  # 2: num_components
    "8d"  # 2: GID of base glyph
    "8b8b"  # 0, 0: offset
    "000000000000f03f000000000000f03f"  # 1.0, 1.0: scale
    "8f"  # 4: GID
    "747f"  # offset
    "000000000000f03f000000000000f03f"  # scale
    "09"  # imported binary
    "29"  # metrics
    "f8d9"  # width
    "ca"  # lsb
    "8b8b8c"  # unknown
    "ca5ef8b6f995"  # bbox
    "2a"  # outlines
    "8a"  # -1: num_contours
    "8b"  # 0: num_endpoint
    "2b"  # instructions
    "8b"  # num_bytes
    "2c"  # HDMX
    "8b"  # num_bytes
    "28"
    "0f"
)

glyph_roundtripped_raw = {
    "name": "uni1E03",
    "num_masters": 1,
    "nodes": [],
    "metrics": [[581, 0]],
    "components": [
        {"gid": 2, "offsetX": [0], "offsetY": [0], "scaleX": [1.0], "scaleY": [1.0]},
        {
            "gid": 4,
            "offsetX": [-23],
            "offsetY": [-12],
            "scaleX": [1.0],
            "scaleY": [1.0],
        },
    ],
    "imported": {
        "width": 581,
        "lsb": 63,
        "unknown1": 0,
        "unknown2": 0,
        "unknown3": 1,
        "bbox": [63, -45, 546, 769],
        "num_contours": -1,
        "endpoints": [],
        "instructions": [],
        "hdmx": [],
    },
}
