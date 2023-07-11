from __future__ import annotations

import pytest

from fontTools.misc.textTools import deHexStr, hexStr
from io import BytesIO
from unittest import TestCase
from vfbLib.compilers.glyph import GlyphCompiler
from vfbLib.parsers.glyph import GlyphParser


psglyph_1master = deHexStr(
    """
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
)

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

psglyph_1master_expected = {
    "constants": (1, 9, 7, 1),
    "name": "d",
    "outlines_value": 490,
    "num_masters": 1,
    "nodes": [
        {"type": "move", "flags": 0, "points": [[(360, 664)]]},
        {"type": "curve", "flags": 1, "points": [[(364, 554), (362, 628), (365, 591)]]},
        {"type": "curve", "flags": 1, "points": [[(346, 312), (362, 473), (351, 393)]]},
        {"type": "curve", "flags": 1, "points": [[(347, 117), (342, 247), (344, 183)]]},
        {"type": "curve", "flags": 0, "points": [[(358, -10), (349, 77), (345, 29)]]},
        {"type": "line", "flags": 0, "points": [[(474, -6)]]},
        {"type": "curve", "flags": 0, "points": [[(475, -3), (475, -5), (475, -4)]]},
        {"type": "curve", "flags": 0, "points": [[(357, 8), (436, 1), (397, 5)]]},
        {"type": "line", "flags": 0, "points": [[(357, 5)]]},
        {"type": "line", "flags": 0, "points": [[(471, 25)]]},
        {"type": "curve", "flags": 1, "points": [[(475, 12), (470, 29), (473, 17)]]},
        {"type": "curve", "flags": 0, "points": [[(473, 21), (476, 10), (474, 18)]]},
        {"type": "line", "flags": 1, "points": [[(469, 55)]]},
        {"type": "curve", "flags": 1, "points": [[(466, 122), (466, 77), (467, 100)]]},
        {"type": "curve", "flags": 0, "points": [[(465, 317), (463, 188), (462, 252)]]},
        {"type": "curve", "flags": 0, "points": [[(479, 669), (476, 435), (483, 551)]]},
        {"type": "move", "flags": 0, "points": [[(452, 287)]]},
        {"type": "curve", "flags": 1, "points": [[(377, 451), (487, 350), (429, 418)]]},
        {"type": "curve", "flags": 1, "points": [[(330, 481), (362, 461), (349, 475)]]},
        {"type": "curve", "flags": 1, "points": [[(60, 376), (228, 515), (109, 474)]]},
        {"type": "curve", "flags": 1, "points": [[(31, 200), (34, 323), (29, 258)]]},
        {"type": "curve", "flags": 1, "points": [[(79, 41), (33, 145), (43, 85)]]},
        {"type": "curve", "flags": 1, "points": [[(292, -2), (123, -12), (230, -26)]]},
        {"type": "curve", "flags": 0, "points": [[(449, 144), (353, 22), (430, 80)]]},
        {"type": "line", "flags": 0, "points": [[(336, 171)]]},
        {"type": "curve", "flags": 0, "points": [[(251, 87), (325, 134), (284, 105)]]},
        {"type": "curve", "flags": 3, "points": [[(239, 86), (247, 87), (243, 86)]]},
        {"type": "curve", "flags": 0, "points": [[(189, 88), (222, 86), (206, 87)]]},
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


class PartCompiler(GlyphCompiler):
    """
    Compile part of the glyph data, by calling the method name passed in compile_method.
    """

    @classmethod
    def _compile(cls, data, num_masters, compile_method):
        cls.stream = BytesIO()
        cls.num_masters = num_masters
        getattr(cls, compile_method)(data)
        return cls.stream.getvalue()


class GlyphCompilerTest(TestCase):
    def test_psglyph_1master_roundtrip(self):
        # Decompile
        dec = GlyphParser.parse(BytesIO(psglyph_1master), len(psglyph_1master))
        assert dec == psglyph_1master_expected

        # Compile
        compiled = GlyphCompiler.compile(dec)
        # print(hexStr(compiled))
        # ... and parse again
        cde = GlyphParser.parse(BytesIO(compiled), len(compiled))
        assert dec == cde

    def test_hints_1(self):
        data = PartCompiler._compile(psglyph_1master_expected, 1, "_compile_hints")
        assert hexStr(data) == hexStr(deHexStr("03    8F  7F C3 F818 C3 F92A 53 85 C2  8D C1 EB F802 E5  8B"))

    def test_metrics_1(self):
        data = PartCompiler._compile(psglyph_1master_expected, 1, "_compile_metrics")
        assert hexStr(data) == "02f8b48b"

    def test_name_1(self):
        data = PartCompiler._compile({"name": "d"}, 1, "_compile_glyph_name")
        assert hexStr(data) == hexStr(deHexStr("01 8C 64"))

    def test_name_2(self):
        data = PartCompiler._compile({"name": "at"}, 1, "_compile_glyph_name")
        assert hexStr(data) == hexStr(deHexStr("01 8D 61 74"))

    def test_outlines_1_master(self):
        data = PartCompiler._compile(psglyph_1master_expected, 1, "_compile_outlines")
        assert hexStr(data) == hexStr(psglyph_1master_nodes)
        assert len(data) == len(psglyph_1master_nodes)  # 285
