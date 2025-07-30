from pathlib import Path
from unittest import TestCase

from fontTools.misc.textTools import deHexStr, hexStr
from fontTools.pens.recordingPen import RecordingPen, RecordingPointPen

from vfbLib.compilers.glyph import GlyphCompiler
from vfbLib.parsers.glyph import GlyphParser
from vfbLib.vfb.entry import VfbEntry
from vfbLib.vfb.glyph import VfbGlyph
from vfbLib.vfb.vfb import Vfb

empty_vfb_path = Path(__file__).parent.parent / "Data" / "empty_522.vfb"


glyph_dict_c = {
    "hints": {
        "h": [],
        "hintmasks": [
            {"v": 2},
            {"h": 0},
            {"h": 1},
            {"h": 2},
            {"v": 0},
            {"r": 2},
            {"v": 1},
            {"h": 2},
            {"v": 0},
            {"h": 0},
            {"h": 1},
            {"r": 11},
            {"v": 2},
            {"h": 0},
            {"h": 1},
            {"h": 2},
            {"v": 0},
            {"r": 12},
            {"v": 1},
            {"h": 1},
            {"v": 0},
            {"h": 0},
            {"h": 2},
            {"r": 18},
            {"v": 2},
            {"h": 0},
            {"v": 0},
            {"h": 1},
            {"h": 2},
        ],
        "v": [],
    },
    "kerning": {
        5: [-19, -23],
        7: [-45, -30],
        17: [10, 3],
        37: [-10, -12],
        38: [7, 2],
        40: [-29, -22],
        41: [-21, -20],
        42: [-38, -35],
        43: [-41, -38],
        47: [-20, -40],
        83: [-30, -30],
        130: [-11, -9],
    },
    "metrics": [(601, 0), (645, 0)],
    "name": "B",
    "nodes": [
        {"flags": 3, "points": [[(566, 210)], [(621, 215)]], "type": "move"},
        {
            "flags": 0,
            "points": [
                [(372, 376), (566, 312), (497, 372)],
                [(434, 382), (621, 317), (558, 376)],
            ],
            "type": "curve",
        },
        {
            "flags": 3,
            "points": [
                [(528, 538), (463, 390), (528, 452)],
                [(583, 536), (525, 398), (583, 454)],
            ],
            "type": "curve",
        },
        {
            "flags": 1,
            "points": [
                [(317, 691), (528, 624), (482, 691)],
                [(343, 691), (583, 630), (521, 691)],
            ],
            "type": "curve",
        },
        {"flags": 0, "points": [[(38, 691)], [(31, 691)]], "type": "line"},
        {"flags": 0, "points": [[(38, 666)], [(31, 650)]], "type": "line"},
        {"flags": 0, "points": [[(114, 639)], [(107, 618)]], "type": "line"},
        {"flags": 0, "points": [[(114, 53)], [(107, 75)]], "type": "line"},
        {"flags": 0, "points": [[(37, 25)], [(30, 41)]], "type": "line"},
        {"flags": 0, "points": [[(37, 0)], [(30, 0)]], "type": "line"},
        {"flags": 1, "points": [[(270, 0)], [(302, 0)]], "type": "line"},
        {
            "flags": 3,
            "points": [
                [(566, 210), (497, 0), (566, 96)],
                [(621, 215), (534, 0), (621, 91)],
            ],
            "type": "curve",
        },
        {"flags": 3, "points": [[(416, 519)], [(417, 513)]], "type": "move"},
        {
            "flags": 1,
            "points": [
                [(290, 387), (416, 445), (380, 387)],
                [(320, 396), (417, 445), (387, 396)],
            ],
            "type": "curve",
        },
        {"flags": 0, "points": [[(222, 387)], [(268, 396)]], "type": "line"},
        {"flags": 0, "points": [[(222, 650)], [(268, 627)]], "type": "line"},
        {"flags": 1, "points": [[(283, 650)], [(313, 627)]], "type": "line"},
        {
            "flags": 3,
            "points": [
                [(416, 519), (366, 650), (416, 611)],
                [(417, 513), (379, 627), (417, 593)],
            ],
            "type": "curve",
        },
        {"flags": 3, "points": [[(452, 198)], [(450, 201)]], "type": "move"},
        {
            "flags": 3,
            "points": [
                [(308, 42), (452, 105), (410, 42)],
                [(337, 65), (450, 116), (415, 65)],
            ],
            "type": "curve",
        },
        {
            "flags": 1,
            "points": [
                [(222, 100), (230, 42), (222, 51)],
                [(268, 121), (279, 65), (268, 76)],
            ],
            "type": "curve",
        },
        {"flags": 0, "points": [[(222, 348)], [(268, 335)]], "type": "line"},
        {"flags": 1, "points": [[(266, 348)], [(306, 335)]], "type": "line"},
        {
            "flags": 3,
            "points": [
                [(452, 198), (392, 348), (452, 297)],
                [(450, 201), (405, 335), (450, 287)],
            ],
            "type": "curve",
        },
    ],
    "num_masters": 2,
}

glyph_dict_q = {
    "guides": {"h": [[], []], "v": [[], []]},
    "metrics": [(550, 0), (550, 0)],
    "name": "B",
    "nodes": [
        {"flags": 0, "points": [[(92, 0)], [(32, 0)]], "type": "move"},
        {"flags": 0, "points": [[(92, 698)], [(32, 698)]], "type": "line"},
        {"flags": 0, "points": [[(277, 698)], [(263, 698)]], "type": "line"},
        {"flags": 0, "points": [[(336, 698)], [(351, 698)]], "type": "qcurve"},
        {"flags": 0, "points": [[(419, 657)], [(465, 658)]], "type": "qcurve"},
        {"flags": 0, "points": [[(461, 579)], [(520, 578)]], "type": "qcurve"},
        {"flags": 0, "points": [[(461, 526)], [(520, 519)]], "type": "line"},
        {"flags": 0, "points": [[(461, 471)], [(520, 469)]], "type": "qcurve"},
        {"flags": 0, "points": [[(420, 391)], [(470, 396)]], "type": "qcurve"},
        {"flags": 0, "points": [[(381, 371)], [(427, 382)]], "type": "line"},
        {"flags": 0, "points": [[(416, 363)], [(463, 375)]], "type": "qcurve"},
        {"flags": 0, "points": [[(472, 314)], [(515, 333)]], "type": "qcurve"},
        {"flags": 0, "points": [[(502, 242)], [(543, 266)]], "type": "qcurve"},
        {"flags": 0, "points": [[(502, 200)], [(543, 223)]], "type": "line"},
        {"flags": 0, "points": [[(502, 138)], [(543, 150)]], "type": "qcurve"},
        {"flags": 0, "points": [[(451, 47)], [(475, 50)]], "type": "qcurve"},
        {"flags": 0, "points": [[(358, 0)], [(343, 0)]], "type": "qcurve"},
        {"flags": 0, "points": [[(296, 0)], [(251, 0)]], "type": "line"},
        {"flags": 0, "points": [[(286, 388)], [(259, 430)]], "type": "move"},
        {"flags": 0, "points": [[(342, 388)], [(285, 430)]], "type": "qcurve"},
        {"flags": 0, "points": [[(398, 454)], [(315, 462)]], "type": "qcurve"},
        {"flags": 0, "points": [[(398, 519)], [(315, 489)]], "type": "line"},
        {"flags": 0, "points": [[(398, 561)], [(315, 508)]], "type": "qcurve"},
        {"flags": 0, "points": [[(369, 618)], [(302, 534)]], "type": "qcurve"},
        {"flags": 0, "points": [[(312, 647)], [(276, 548)]], "type": "qcurve"},
        {"flags": 0, "points": [[(269, 647)], [(257, 548)]], "type": "line"},
        {"flags": 0, "points": [[(151, 647)], [(235, 548)]], "type": "line"},
        {"flags": 0, "points": [[(151, 388)], [(235, 430)]], "type": "line"},
        {"flags": 0, "points": [[(301, 51)], [(267, 154)]], "type": "move"},
        {"flags": 0, "points": [[(342, 51)], [(286, 154)]], "type": "qcurve"},
        {"flags": 0, "points": [[(405, 85)], [(313, 168)]], "type": "qcurve"},
        {"flags": 0, "points": [[(439, 148)], [(327, 196)]], "type": "qcurve"},
        {"flags": 0, "points": [[(439, 192)], [(327, 217)]], "type": "line"},
        {"flags": 0, "points": [[(439, 263)], [(327, 252)]], "type": "qcurve"},
        {"flags": 0, "points": [[(360, 338)], [(294, 284)]], "type": "qcurve"},
        {"flags": 0, "points": [[(284, 338)], [(260, 284)]], "type": "line"},
        {"flags": 0, "points": [[(151, 338)], [(235, 284)]], "type": "line"},
        {"flags": 0, "points": [[(151, 51)], [(235, 154)]], "type": "line"},
    ],
    "num_masters": 2,
    "tth": [
        {"cmd": "AlignH", "params": {"align": 0, "pt": 38}},
        {"cmd": "AlignH", "params": {"align": 0, "pt": 39}},
        {
            "cmd": "SingleLinkH",
            "params": {"align": -1, "pt1": 38, "pt2": 0, "stem": -2},
        },
        {"cmd": "MDeltaH", "params": {"ppm1": 22, "ppm2": 22, "pt": 0, "shift": -8}},
        {
            "cmd": "SingleLinkH",
            "params": {"align": 0, "pt1": 39, "pt2": 13, "stem": -1},
        },
        {"cmd": "MDeltaH", "params": {"ppm1": 10, "ppm2": 10, "pt": 13, "shift": -8}},
        {"cmd": "MDeltaH", "params": {"ppm1": 12, "ppm2": 12, "pt": 13, "shift": -8}},
        {"cmd": "InterpolateH", "params": {"align": 0, "pt1": 13, "pt2": 0, "pti": 6}},
        {"cmd": "InterpolateH", "params": {"align": -1, "pt1": 13, "pt2": 0, "pti": 9}},
        {"cmd": "SingleLinkH", "params": {"align": -1, "pt1": 6, "pt2": 21, "stem": 0}},
        {"cmd": "SingleLinkH", "params": {"align": -1, "pt1": 0, "pt2": 37, "stem": 0}},
        {
            "cmd": "SingleLinkH",
            "params": {"align": -1, "pt1": 37, "pt2": 27, "stem": -1},
        },
        {
            "cmd": "SingleLinkH",
            "params": {"align": -1, "pt1": 13, "pt2": 32, "stem": 0},
        },
        {"cmd": "AlignTop", "params": {"pt": 1, "zone": 4}},
        {"cmd": "AlignBottom", "params": {"pt": 0, "zone": 0}},
        {"cmd": "InterpolateV", "params": {"align": 0, "pt1": 1, "pt2": 0, "pti": 36}},
        {
            "cmd": "SingleLinkV",
            "params": {"align": -1, "pt1": 36, "pt2": 27, "stem": 0},
        },
        {
            "cmd": "InterpolateV",
            "params": {"align": -1, "pt1": 27, "pt2": 36, "pti": 9},
        },
        {"cmd": "SingleLinkV", "params": {"align": -1, "pt1": 1, "pt2": 26, "stem": 0}},
        {"cmd": "SingleLinkV", "params": {"align": -1, "pt1": 0, "pt2": 37, "stem": 0}},
    ],
}


glyph_nodes_q_1m = [
    {"flags": 0, "points": [[(92, 0)]], "type": "move"},
    {"flags": 0, "points": [[(92, 698)]], "type": "line"},
    {"flags": 0, "points": [[(277, 698)]], "type": "line"},
    {"flags": 0, "points": [[(336, 698)]], "type": "qcurve"},
    {"flags": 0, "points": [[(419, 657)]], "type": "qcurve"},
    {"flags": 0, "points": [[(461, 579)]], "type": "qcurve"},
    {"flags": 0, "points": [[(461, 526)]], "type": "line"},
    {"flags": 0, "points": [[(461, 471)]], "type": "qcurve"},
    {"flags": 0, "points": [[(420, 391)]], "type": "qcurve"},
    {"flags": 0, "points": [[(381, 371)]], "type": "line"},
    {"flags": 0, "points": [[(416, 363)]], "type": "qcurve"},
    {"flags": 0, "points": [[(472, 314)]], "type": "qcurve"},
    {"flags": 0, "points": [[(502, 242)]], "type": "qcurve"},
    {"flags": 0, "points": [[(502, 200)]], "type": "line"},
    {"flags": 0, "points": [[(502, 138)]], "type": "qcurve"},
    {"flags": 0, "points": [[(451, 47)]], "type": "qcurve"},
    {"flags": 0, "points": [[(358, 0)]], "type": "qcurve"},
    {"flags": 0, "points": [[(296, 0)]], "type": "line"},
    {"flags": 0, "points": [[(286, 388)]], "type": "move"},
    {"flags": 0, "points": [[(342, 388)]], "type": "qcurve"},
    {"flags": 0, "points": [[(398, 454)]], "type": "qcurve"},
    {"flags": 0, "points": [[(398, 519)]], "type": "line"},
    {"flags": 0, "points": [[(398, 561)]], "type": "qcurve"},
    {"flags": 0, "points": [[(369, 618)]], "type": "qcurve"},
    {"flags": 0, "points": [[(312, 647)]], "type": "qcurve"},
    {"flags": 0, "points": [[(269, 647)]], "type": "line"},
    {"flags": 0, "points": [[(151, 647)]], "type": "line"},
    {"flags": 0, "points": [[(151, 388)]], "type": "line"},
    {"flags": 0, "points": [[(301, 51)]], "type": "move"},
    {"flags": 0, "points": [[(342, 51)]], "type": "qcurve"},
    {"flags": 0, "points": [[(405, 85)]], "type": "qcurve"},
    {"flags": 0, "points": [[(439, 148)]], "type": "qcurve"},
    {"flags": 0, "points": [[(439, 192)]], "type": "line"},
    {"flags": 0, "points": [[(439, 263)]], "type": "qcurve"},
    {"flags": 0, "points": [[(360, 338)]], "type": "qcurve"},
    {"flags": 0, "points": [[(284, 338)]], "type": "line"},
    {"flags": 0, "points": [[(151, 338)]], "type": "line"},
    {"flags": 0, "points": [[(151, 51)]], "type": "line"},
]


class VfbGlyphTest(TestCase):
    def test_drawPoints_quadratic(self):
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb), vfb)
        g.entry.data = glyph_dict_q
        pen = RecordingPointPen()
        g.drawPoints(pen)
        assert pen.value == [
            ("beginPath", (), {}),
            ("addPoint", ((92, 0), "line", False, None), {}),
            ("addPoint", ((92, 698), "line", False, None), {}),
            ("addPoint", ((277, 698), "line", False, None), {}),
            ("addPoint", ((336, 698), None, False, None), {}),
            ("addPoint", ((419, 657), None, False, None), {}),
            ("addPoint", ((461, 579), None, False, None), {}),
            ("addPoint", ((461, 526), "qcurve", False, None), {}),
            ("addPoint", ((461, 471), None, False, None), {}),
            ("addPoint", ((420, 391), None, False, None), {}),
            ("addPoint", ((381, 371), "qcurve", False, None), {}),
            ("addPoint", ((416, 363), None, False, None), {}),
            ("addPoint", ((472, 314), None, False, None), {}),
            ("addPoint", ((502, 242), None, False, None), {}),
            ("addPoint", ((502, 200), "qcurve", False, None), {}),
            ("addPoint", ((502, 138), None, False, None), {}),
            ("addPoint", ((451, 47), None, False, None), {}),
            ("addPoint", ((358, 0), None, False, None), {}),
            ("addPoint", ((296, 0), "qcurve", False, None), {}),
            ("endPath", (), {}),
            ("beginPath", (), {}),
            ("addPoint", ((286, 388), "line", False, None), {}),
            ("addPoint", ((342, 388), None, False, None), {}),
            ("addPoint", ((398, 454), None, False, None), {}),
            ("addPoint", ((398, 519), "qcurve", False, None), {}),
            ("addPoint", ((398, 561), None, False, None), {}),
            ("addPoint", ((369, 618), None, False, None), {}),
            ("addPoint", ((312, 647), None, False, None), {}),
            ("addPoint", ((269, 647), "qcurve", False, None), {}),
            ("addPoint", ((151, 647), "line", False, None), {}),
            ("addPoint", ((151, 388), "line", False, None), {}),
            ("endPath", (), {}),
            ("beginPath", (), {}),
            ("addPoint", ((301, 51), "line", False, None), {}),
            ("addPoint", ((342, 51), None, False, None), {}),
            ("addPoint", ((405, 85), None, False, None), {}),
            ("addPoint", ((439, 148), None, False, None), {}),
            ("addPoint", ((439, 192), "qcurve", False, None), {}),
            ("addPoint", ((439, 263), None, False, None), {}),
            ("addPoint", ((360, 338), None, False, None), {}),
            ("addPoint", ((284, 338), "qcurve", False, None), {}),
            ("addPoint", ((151, 338), "line", False, None), {}),
            ("addPoint", ((151, 51), "line", False, None), {}),
            ("endPath", (), {}),
        ]

        # TODO: Support names from TrueType hinting?
        # with_labels = [
        #     ("beginPath", (), {}),
        #     ("addPoint", ((92, 0), "line", False, "sh01"), {}),
        #     ("addPoint", ((92, 698), "line", False, "at01"), {}),
        #     ("addPoint", ((277, 698), "line", False, None), {}),
        #     ("addPoint", ((336, 698), None, False, None), {}),
        #     ("addPoint", ((419, 657), None, False, None), {}),
        #     ("addPoint", ((461, 579), None, False, None), {}),
        #     ("addPoint", ((461, 526), "qcurve", False, "ih01"), {}),
        #     ("addPoint", ((461, 471), None, False, None), {}),
        #     ("addPoint", ((420, 391), None, False, None), {}),
        #     ("addPoint", ((381, 371), "qcurve", False, "ih02"), {}),
        #     ("addPoint", ((416, 363), None, False, None), {}),
        #     ("addPoint", ((472, 314), None, False, None), {}),
        #     ("addPoint", ((502, 242), None, False, None), {}),
        #     ("addPoint", ((502, 200), "qcurve", False, "sh02"), {}),
        #     ("addPoint", ((502, 138), None, False, None), {}),
        #     ("addPoint", ((451, 47), None, False, None), {}),
        #     ("addPoint", ((358, 0), None, False, None), {}),
        #     ("addPoint", ((296, 0), "qcurve", False, None), {}),
        #     ("endPath", (), {}),
        #     ("beginPath", (), {}),
        #     ("addPoint", ((286, 388), "line", False, None), {}),
        #     ("addPoint", ((342, 388), None, False, None), {}),
        #     ("addPoint", ((398, 454), None, False, None), {}),
        #     ("addPoint", ((398, 519), "qcurve", False, "sh03"), {}),
        #     ("addPoint", ((398, 561), None, False, None), {}),
        #     ("addPoint", ((369, 618), None, False, None), {}),
        #     ("addPoint", ((312, 647), None, False, None), {}),
        #     ("addPoint", ((269, 647), "qcurve", False, None), {}),
        #     ("addPoint", ((151, 647), "line", False, "sv01"), {}),
        #     ("addPoint", ((151, 388), "line", False, "sh05"), {}),
        #     ("endPath", (), {}),
        #     ("beginPath", (), {}),
        #     ("addPoint", ((301, 51), "line", False, None), {}),
        #     ("addPoint", ((342, 51), None, False, None), {}),
        #     ("addPoint", ((405, 85), None, False, None), {}),
        #     ("addPoint", ((439, 148), None, False, None), {}),
        #     ("addPoint", ((439, 192), "qcurve", False, "sh06"), {}),
        #     ("addPoint", ((439, 263), None, False, None), {}),
        #     ("addPoint", ((360, 338), None, False, None), {}),
        #     ("addPoint", ((284, 338), "qcurve", False, None), {}),
        #     ("addPoint", ((151, 338), "line", False, "iv01"), {}),
        #     ("addPoint", ((151, 51), "line", False, "sh04"), {}),
        #     ("endPath", (), {}),
        # ]

    def test_draw_quadratic(self):
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb), vfb)
        g.entry.data = glyph_dict_q
        pen = RecordingPen()
        g.draw(pen)
        assert pen.value == [
            ("moveTo", ((92, 0),)),
            ("lineTo", ((92, 698),)),
            ("lineTo", ((277, 698),)),
            ("qCurveTo", ((336, 698), (419, 657), (461, 579), (461, 526))),
            ("qCurveTo", ((461, 471), (420, 391), (381, 371))),
            ("qCurveTo", ((416, 363), (472, 314), (502, 242), (502, 200))),
            ("qCurveTo", ((502, 138), (451, 47), (358, 0), (296, 0))),
            ("closePath", ()),
            ("moveTo", ((286, 388),)),
            ("qCurveTo", ((342, 388), (398, 454), (398, 519))),
            ("qCurveTo", ((398, 561), (369, 618), (312, 647), (269, 647))),
            ("lineTo", ((151, 647),)),
            ("lineTo", ((151, 388),)),
            ("closePath", ()),
            ("moveTo", ((301, 51),)),
            ("qCurveTo", ((342, 51), (405, 85), (439, 148), (439, 192))),
            ("qCurveTo", ((439, 263), (360, 338), (284, 338))),
            ("lineTo", ((151, 338),)),
            ("lineTo", ((151, 51),)),
            ("closePath", ()),
        ]

    def test_drawPoints_cubic(self):
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb), vfb)
        g.entry.data = glyph_dict_c
        pen = RecordingPointPen()
        g.drawPoints(pen)
        assert pen.value == [
            ("beginPath", (), {}),
            ("addPoint", ((566, 210), "curve", True, None), {}),
            ("addPoint", ((566, 312), None, False, None), {}),
            ("addPoint", ((497, 372), None, False, None), {}),
            ("addPoint", ((372, 376), "curve", False, None), {}),
            ("addPoint", ((463, 390), None, False, None), {}),
            ("addPoint", ((528, 452), None, False, None), {}),
            ("addPoint", ((528, 538), "curve", True, None), {}),
            ("addPoint", ((528, 624), None, False, None), {}),
            ("addPoint", ((482, 691), None, False, None), {}),
            ("addPoint", ((317, 691), "curve", True, None), {}),
            ("addPoint", ((38, 691), "line", False, None), {}),
            ("addPoint", ((38, 666), "line", False, None), {}),
            ("addPoint", ((114, 639), "line", False, None), {}),
            ("addPoint", ((114, 53), "line", False, None), {}),
            ("addPoint", ((37, 25), "line", False, None), {}),
            ("addPoint", ((37, 0), "line", False, None), {}),
            ("addPoint", ((270, 0), "line", True, None), {}),
            ("addPoint", ((497, 0), None, False, None), {}),
            ("addPoint", ((566, 96), None, False, None), {}),
            ("endPath", (), {}),
            ("beginPath", (), {}),
            ("addPoint", ((416, 519), "curve", True, None), {}),
            ("addPoint", ((416, 445), None, False, None), {}),
            ("addPoint", ((380, 387), None, False, None), {}),
            ("addPoint", ((290, 387), "curve", True, None), {}),
            ("addPoint", ((222, 387), "line", False, None), {}),
            ("addPoint", ((222, 650), "line", False, None), {}),
            ("addPoint", ((283, 650), "line", True, None), {}),
            ("addPoint", ((366, 650), None, False, None), {}),
            ("addPoint", ((416, 611), None, False, None), {}),
            ("endPath", (), {}),
            ("beginPath", (), {}),
            ("addPoint", ((452, 198), "curve", True, None), {}),
            ("addPoint", ((452, 105), None, False, None), {}),
            ("addPoint", ((410, 42), None, False, None), {}),
            ("addPoint", ((308, 42), "curve", True, None), {}),
            ("addPoint", ((230, 42), None, False, None), {}),
            ("addPoint", ((222, 51), None, False, None), {}),
            ("addPoint", ((222, 100), "curve", True, None), {}),
            ("addPoint", ((222, 348), "line", False, None), {}),
            ("addPoint", ((266, 348), "line", True, None), {}),
            ("addPoint", ((392, 348), None, False, None), {}),
            ("addPoint", ((452, 297), None, False, None), {}),
            ("endPath", (), {}),
        ]

    def test_draw_cubic(self):
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb), vfb)
        g.entry.data = glyph_dict_c
        pen = RecordingPen()
        g.draw(pen)
        assert pen.value == [
            ("moveTo", ((566, 210),)),
            ("curveTo", ((566, 312), (497, 372), (372, 376))),
            ("curveTo", ((463, 390), (528, 452), (528, 538))),
            ("curveTo", ((528, 624), (482, 691), (317, 691))),
            ("lineTo", ((38, 691),)),
            ("lineTo", ((38, 666),)),
            ("lineTo", ((114, 639),)),
            ("lineTo", ((114, 53),)),
            ("lineTo", ((37, 25),)),
            ("lineTo", ((37, 0),)),
            ("lineTo", ((270, 0),)),
            ("curveTo", ((497, 0), (566, 96), (566, 210))),
            ("closePath", ()),
            ("moveTo", ((416, 519),)),
            ("curveTo", ((416, 445), (380, 387), (290, 387))),
            ("lineTo", ((222, 387),)),
            ("lineTo", ((222, 650),)),
            ("lineTo", ((283, 650),)),
            ("curveTo", ((366, 650), (416, 611), (416, 519))),
            ("closePath", ()),
            ("moveTo", ((452, 198),)),
            ("curveTo", ((452, 105), (410, 42), (308, 42))),
            ("curveTo", ((230, 42), (222, 51), (222, 100))),
            ("lineTo", ((222, 348),)),
            ("lineTo", ((266, 348),)),
            ("curveTo", ((392, 348), (452, 297), (452, 198))),
            ("closePath", ()),
        ]

    def test_getPointPen_simple(self):
        # Get a point pen and draw into the vfb glyph
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb, parser=GlyphParser, compiler=GlyphCompiler), vfb)
        pen = g.getPointPen()
        pen.beginPath()
        pen.addPoint(pt=(100, 100), segmentType="line", smooth=False)
        pen.addPoint(pt=(200, 100), segmentType="line", smooth=False)
        pen.addPoint(pt=(200, 200), segmentType="line", smooth=False)
        pen.addPoint(pt=(100, 150), segmentType="line", smooth=False)
        pen.endPath()
        assert g.entry.data["nodes"] == [
            {"flags": 0, "points": [[(100, 100)]], "type": "move"},
            {"flags": 0, "points": [[(200, 100)]], "type": "line"},
            {"flags": 0, "points": [[(200, 200)]], "type": "line"},
            {"flags": 0, "points": [[(100, 150)]], "type": "line"},
        ]

    def test_getPointPen_simple_compile(self):
        # Get a point pen and draw into the vfb glyph
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb, parser=GlyphParser, compiler=GlyphCompiler), vfb)
        g.entry.data["name"] = "a"
        g.entry.data["metrics"] = [(833, 0)]
        pen = g.getPointPen()
        pen.beginPath()
        pen.addPoint(pt=(100, 100), segmentType="line", smooth=False)
        pen.addPoint(pt=(200, 100), segmentType="line", smooth=False)
        pen.addPoint(pt=(200, 200), segmentType="line", smooth=False)
        pen.addPoint(pt=(100, 150), segmentType="line", smooth=False)
        pen.endPath()
        g.entry.compile()
        assert (
            hexStr(g.entry.data)
            == "01090701018c61088ca38f00efef01ef8b018bef01275902f9d58b0f"  # 038b8b8b0f
        )

    def test_getPointPen_simple_decompile(self):
        # Get a point pen and draw into the vfb glyph
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb, parser=GlyphParser, compiler=GlyphCompiler), vfb)
        g.entry.data["name"] = "a"
        g.entry.data["metrics"] = [(833, 0)]
        pen = g.getPointPen()
        pen.beginPath()
        pen.addPoint(pt=(100, 100), segmentType="line", smooth=False)
        pen.addPoint(pt=(200, 100), segmentType="line", smooth=False)
        pen.addPoint(pt=(200, 200), segmentType="line", smooth=False)
        pen.addPoint(pt=(100, 150), segmentType="line", smooth=False)
        pen.endPath()
        expected = VfbEntry(vfb, GlyphParser)
        expected.data = deHexStr(
            "01090701018c61088ca38f00efef01ef8b018bef01275902f9d58b0f"
        )
        expected.decompile()
        g.entry.compile()
        g.entry.decompile()
        # print(g.entry.data)
        assert expected.data == g.entry.data

    def test_getPointPen_quadratic_1_master(self):
        # Get a point pen and draw into the vfb glyph
        vfb = Vfb(empty_vfb_path)
        g = VfbGlyph(VfbEntry(vfb, parser=GlyphParser, compiler=GlyphCompiler), vfb)
        pen = g.getPointPen()
        pen.beginPath()
        pen.addPoint((92, 0), "line", False, None)
        pen.addPoint((92, 698), "line", False, None)
        pen.addPoint((277, 698), "line", False, None)
        pen.addPoint((336, 698), None, False, None)
        pen.addPoint((419, 657), None, False, None)
        pen.addPoint((461, 579), None, False, None)
        pen.addPoint((461, 526), "qcurve", False, None)
        pen.addPoint((461, 471), None, False, None)
        pen.addPoint((420, 391), None, False, None)
        pen.addPoint((381, 371), "qcurve", False, None)
        pen.addPoint((416, 363), None, False, None)
        pen.addPoint((472, 314), None, False, None)
        pen.addPoint((502, 242), None, False, None)
        pen.addPoint((502, 200), "qcurve", False, None)
        pen.addPoint((502, 138), None, False, None)
        pen.addPoint((451, 47), None, False, None)
        pen.addPoint((358, 0), None, False, None)
        pen.addPoint((296, 0), "qcurve", False, None)
        pen.endPath()
        pen.beginPath()
        pen.addPoint((286, 388), "line", False, None)
        pen.addPoint((342, 388), None, False, None)
        pen.addPoint((398, 454), None, False, None)
        pen.addPoint((398, 519), "qcurve", False, None)
        pen.addPoint((398, 561), None, False, None)
        pen.addPoint((369, 618), None, False, None)
        pen.addPoint((312, 647), None, False, None)
        pen.addPoint((269, 647), "qcurve", False, None)
        pen.addPoint((151, 647), "line", False, None)
        pen.addPoint((151, 388), "line", False, None)
        pen.endPath()
        pen.beginPath()
        pen.addPoint((301, 51), "line", False, None)
        pen.addPoint((342, 51), None, False, None)
        pen.addPoint((405, 85), None, False, None)
        pen.addPoint((439, 148), None, False, None)
        pen.addPoint((439, 192), "qcurve", False, None)
        pen.addPoint((439, 263), None, False, None)
        pen.addPoint((360, 338), None, False, None)
        pen.addPoint((284, 338), "qcurve", False, None)
        pen.addPoint((151, 338), "line", False, None)
        pen.addPoint((151, 51), "line", False, None)
        pen.endPath()
        assert g.entry.data["nodes"] == glyph_nodes_q_1m
        g.entry.compile()  # XXX: Hack
        g.entry.decompile()
        assert g.entry.data["nodes"] == glyph_nodes_q_1m

    def test_getPointPenMM(self):
        # FIXME
        pass

    def test_getPointPen_empty(self):
        # FIXME
        pass
