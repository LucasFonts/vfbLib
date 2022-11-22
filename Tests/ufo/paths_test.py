from unittest import TestCase

from pprint import pprint
from vfbLib.ufo.paths import get_master_glyph


closed_path = [
    {"type": "move", "flags": 3, "points": [[{"x": 92, "y": 365}]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 364, "y": 86}, {"x": 92, "y": 210}, {"x": 214, "y": 86}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 636, "y": 365}, {"x": 514, "y": 86}, {"x": 636, "y": 210}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 364, "y": 645}, {"x": 636, "y": 520}, {"x": 514, "y": 645}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 92, "y": 365}, {"x": 214, "y": 645}, {"x": 92, "y": 520}]
        ],
    },
    {"type": "move", "flags": 0, "points": [[{"x": 259, "y": 347}]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 396, "y": 490}, {"x": 259, "y": 426}, {"x": 320, "y": 490}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 534, "y": 347}, {"x": 472, "y": 490}, {"x": 534, "y": 426}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 396, "y": 205}, {"x": 534, "y": 268}, {"x": 472, "y": 205}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 259, "y": 347}, {"x": 320, "y": 205}, {"x": 259, "y": 268}]
        ],
    },
]

open_path = [
    {"type": "move", "flags": 11, "points": [[{"x": 92, "y": 365}]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 364, "y": 86}, {"x": 92, "y": 210}, {"x": 214, "y": 86}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 636, "y": 365}, {"x": 514, "y": 86}, {"x": 636, "y": 210}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 364, "y": 645}, {"x": 636, "y": 520}, {"x": 514, "y": 645}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 92, "y": 365}, {"x": 214, "y": 645}, {"x": 92, "y": 520}]
        ],
    },
    {"type": "move", "flags": 0, "points": [[{"x": 259, "y": 347}]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 396, "y": 490}, {"x": 259, "y": 426}, {"x": 320, "y": 490}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 534, "y": 347}, {"x": 472, "y": 490}, {"x": 534, "y": 426}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 396, "y": 205}, {"x": 534, "y": 268}, {"x": 472, "y": 205}]
        ],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [
            [{"x": 259, "y": 347}, {"x": 320, "y": 205}, {"x": 259, "y": 268}]
        ],
    },
]

open_path_tt = [
    {"type": "move", "flags": 8, "points": [[{"x": 92, "y": 365}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 92, "y": 249}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 251, "y": 86}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 364, "y": 86}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 477, "y": 86}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 636, "y": 249}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 636, "y": 365}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 636, "y": 481}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 477, "y": 645}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 364, "y": 645}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 251, "y": 645}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 92, "y": 481}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 92, "y": 365}]]},
    {"type": "move", "flags": 0, "points": [[{"x": 259, "y": 347}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 259, "y": 406}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 339, "y": 490}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 396, "y": 490}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 453, "y": 490}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 534, "y": 406}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 534, "y": 347}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 534, "y": 288}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 453, "y": 205}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 396, "y": 205}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 339, "y": 205}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 259, "y": 288}]]},
]

open_path_line = [
    {"type": "move", "flags": 8, "points": [[{"x": 172, "y": 163}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 395, "y": 163}]]},
    {
        "type": "curve",
        "flags": 0,
        "points": [
            [{"x": 172, "y": 612}, {"x": 395, "y": 360}, {"x": 290, "y": 612}]
        ],
    },
    {"type": "line", "flags": 0, "points": [[{"x": 172, "y": 163}]]},
    {"type": "move", "flags": 8, "points": [[{"x": 505, "y": 152}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 589, "y": 152}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 598, "y": 202}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 602, "y": 310}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 594, "y": 412}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 577, "y": 503}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 552, "y": 572}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 521, "y": 612}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 505, "y": 612}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 505, "y": 152}]]},
    {"type": "move", "flags": 0, "points": [[{"x": 645, "y": 113}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 740, "y": 113}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 645, "y": 603}]]},
]

closed_path_line = [
    {"type": "move",   "flags": 0, "points": [[{"x": 172, "y": 163}]]},
    {"type": "line",   "flags": 0, "points": [[{"x": 395, "y": 163}]]},
    {"type": "curve",  "flags": 0, "points": [[{"x": 172, "y": 612}, {"x": 395, "y": 360}, {"x": 290, "y": 612}]]},

    {"type": "move",   "flags": 0, "points": [[{"x": 505, "y": 152}]]},
    {"type": "line",   "flags": 0, "points": [[{"x": 589, "y": 152}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 598, "y": 202}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 602, "y": 310}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 594, "y": 412}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 577, "y": 503}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 552, "y": 572}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 521, "y": 612}]]},
    {"type": "line",   "flags": 0, "points": [[{"x": 505, "y": 612}]]},

    {"type": "move",   "flags": 0, "points": [[{"x": 645, "y": 113}]]},
    {"type": "line",   "flags": 0, "points": [[{"x": 740, "y": 113}]]},
    {"type": "line",   "flags": 0, "points": [[{"x": 645, "y": 603}]]},
]

complex_tt = [
    {"type": "move", "flags": 0, "points": [[{"x": 199, "y": -12}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 124, "y": -12}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 43, "y": 64}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 43, "y": 130}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 43, "y": 204}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 149, "y": 282}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 274, "y": 282}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 347, "y": 282}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 347, "y": 355}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 347, "y": 416}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 290, "y": 480}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 232, "y": 480}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 207, "y": 480}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 166, "y": 472}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 152, "y": 464}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 152, "y": 462}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 163, "y": 456}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 183, "y": 432}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 183, "y": 410}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 183, "y": 383}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 152, "y": 352}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 125, "y": 352}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 99, "y": 352}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 67, "y": 384}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 67, "y": 413}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 67, "y": 435}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 93, "y": 477}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 143, "y": 510}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 216, "y": 530}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 263, "y": 530}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 351, "y": 530}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 443, "y": 444}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 443, "y": 366}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 443, "y": 47}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 515, "y": 47}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 515, "y": 8}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 502, "y": 0}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 462, "y": -12}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 438, "y": -12}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 395, "y": -12}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 352, "y": 33}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 352, "y": 71}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 352, "y": 77}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 348, "y": 77}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 341, "y": 60}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 318, "y": 28}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 283, "y": 3}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 233, "y": -12}]]},
    {"type": "move", "flags": 0, "points": [[{"x": 238, "y": 50}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 284, "y": 50}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 347, "y": 96}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 347, "y": 145}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 347, "y": 239}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 284, "y": 239}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 206, "y": 239}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 146, "y": 190}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 146, "y": 145}]]},
    {"type": "line", "flags": 0, "points": [[{"x": 146, "y": 125}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 146, "y": 87}]]},
    {"type": "qcurve", "flags": 0, "points": [[{"x": 195, "y": 50}]]},
]


class MMGlyph:
    def __init__(self, paths):
        self.mm_nodes = paths


class PathsTest(TestCase):
    def test_closed_path(self):
        contours, components = get_master_glyph(MMGlyph(closed_path), [], 0)
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["curve", 3, (92, 365)],
            [None, 3, (92, 210)],
            [None, 3, (214, 86)],
            ["curve", 3, (364, 86)],
            [None, 3, (514, 86)],
            [None, 3, (636, 210)],
            ["curve", 3, (636, 365)],
            [None, 3, (636, 520)],
            [None, 3, (514, 645)],
            ["curve", 3, (364, 645)],
            [None, 3, (214, 645)],
            [None, 3, (92, 520)],
        ]
        assert contours[1] == [
            ["curve", 3, (259, 347)],
            [None, 3, (259, 426)],
            [None, 3, (320, 490)],
            ["curve", 3, (396, 490)],
            [None, 3, (472, 490)],
            [None, 3, (534, 426)],
            ["curve", 3, (534, 347)],
            [None, 3, (534, 268)],
            [None, 3, (472, 205)],
            ["curve", 3, (396, 205)],
            [None, 3, (320, 205)],
            [None, 3, (259, 268)],
        ]

    # def test_open_path(self):
    #     contours, components = get_master_glyph(MMGlyph(open_path), [], 0)
    #     assert components == []
    #     assert contours[0] == [
    #         ["move", 11, (92, 365)],
    #         [None, 3, (92, 210)],
    #         [None, 3, (214, 86)],
    #         ["curve", 3, (364, 86)],
    #         [None, 3, (514, 86)],
    #         [None, 3, (636, 210)],
    #         ["curve", 3, (636, 365)],
    #         [None, 3, (636, 520)],
    #         [None, 3, (514, 645)],
    #         ["curve", 3, (364, 645)],
    #         [None, 3, (214, 645)],
    #         [None, 3, (92, 520)],
    #         ["curve", 3, (92, 365)],
    #     ]
    #     assert contours[1] == [
    #         ["curve", 3, (259, 347)],
    #         [None, 3, (259, 426)],
    #         [None, 3, (320, 490)],
    #         ["curve", 3, (396, 490)],
    #         [None, 3, (472, 490)],
    #         [None, 3, (534, 426)],
    #         ["curve", 3, (534, 347)],
    #         [None, 3, (534, 268)],
    #         [None, 3, (472, 205)],
    #         ["curve", 3, (396, 205)],
    #         [None, 3, (320, 205)],
    #         [None, 3, (259, 268)],
    #     ]

    # def test_open_tt_path(self):
    #     contours, components = get_master_glyph(MMGlyph(open_path_tt), [], 0)
    #     assert components == []
    #     pprint(contours[1])
    #     assert contours[0] == [
    #         ["move", 8, (92, 365)],
    #         [None, 0, (92, 249)],
    #         [None, 0, (251, 86)],
    #         ["qcurve", 0, (364, 86)],
    #         [None, 0, (477, 86)],
    #         [None, 0, (636, 249)],
    #         ["qcurve", 0, (636, 365)],
    #         [None, 0, (636, 481)],
    #         [None, 0, (477, 645)],
    #         ["qcurve", 0, (364, 645)],
    #         [None, 0, (251, 645)],
    #         [None, 0, (92, 481)],
    #         ["qcurve", 0, (92, 365)],
    #     ]
    #     assert contours[1] == [
    #         ["qcurve", 0, (259, 347)],
    #         [None, 0, (259, 406)],
    #         [None, 0, (339, 490)],
    #         ["qcurve", 0, (396, 490)],
    #         [None, 0, (453, 490)],
    #         [None, 0, (534, 406)],
    #         ["qcurve", 0, (534, 347)],
    #         [None, 0, (534, 288)],
    #         [None, 0, (453, 205)],
    #         ["qcurve", 0, (396, 205)],
    #         [None, 0, (339, 205)],
    #         [None, 0, (259, 288)],
    #     ]

    def test_closed_line_path(self):
        contours, components = get_master_glyph(
            MMGlyph(closed_path_line), [], 0
        )
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["line", 0, (172, 163)],
            ["line", 0, (395, 163)],
            [None, 0, (395, 360)],
            [None, 0, (290, 612)],
            ["curve", 0, (172, 612)],
        ]
        assert contours[1] == [
            ["line", 0, (505, 152)],
            ["line", 0, (589, 152)],
            [None, 0, (598, 202)],
            [None, 0, (602, 310)],
            [None, 0, (594, 412)],
            [None, 0, (577, 503)],
            [None, 0, (552, 572)],
            [None, 0, (521, 612)],
            ["qcurve", 0, (505, 612)],
        ]
        assert contours[2] == [
            ["line", 0, (645, 113)],
            ["line", 0, (740, 113)],
            ["line", 0, (645, 603)],
        ]

    def test_open_line_path(self):
        contours, components = get_master_glyph(MMGlyph(open_path_line), [], 0)
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["move", 8, (172, 163)],
            ["line", 0, (395, 163)],
            [None, 0, (395, 360)],
            [None, 0, (290, 612)],
            ["curve", 0, (172, 612)],
            ["line", 0, (172, 163)],
        ]
        assert contours[1] == [
            ["move", 8, (505, 152)],
            ["line", 0, (589, 152)],
            [None, 0, (598, 202)],
            [None, 0, (602, 310)],
            [None, 0, (594, 412)],
            [None, 0, (577, 503)],
            [None, 0, (552, 572)],
            [None, 0, (521, 612)],
            ["qcurve", 0, (505, 612)],
            ["line", 0, (505, 152)],
        ]
        assert contours[2] == [
            ["line", 0, (645, 113)],
            ["line", 0, (740, 113)],
            ["line", 0, (645, 603)],
        ]

    def test_complex_tt(self):
        contours, components = get_master_glyph(MMGlyph(complex_tt), [], 0)
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["qcurve", 0, (199, -12)],  # was "move"
            [None, 0, (124, -12)],
            [None, 0, (43, 64)],
            ["qcurve", 0, (43, 130)],
            [None, 0, (43, 204)],
            [None, 0, (149, 282)],
            ["qcurve", 0, (274, 282)],
            ["line", 0, (347, 282)],
            ["line", 0, (347, 355)],
            [None, 0, (347, 416)],
            [None, 0, (290, 480)],
            ["qcurve", 0, (232, 480)],
            [None, 0, (207, 480)],
            [None, 0, (166, 472)],
            ["qcurve", 0, (152, 464)],
            ["line", 0, (152, 462)],
            [None, 0, (163, 456)],
            [None, 0, (183, 432)],
            ["qcurve", 0, (183, 410)],
            [None, 0, (183, 383)],
            [None, 0, (152, 352)],
            ["qcurve", 0, (125, 352)],
            [None, 0, (99, 352)],
            [None, 0, (67, 384)],
            ["qcurve", 0, (67, 413)],
            [None, 0, (67, 435)],
            [None, 0, (93, 477)],
            [None, 0, (143, 510)],
            [None, 0, (216, 530)],
            ["qcurve", 0, (263, 530)],
            [None, 0, (351, 530)],
            [None, 0, (443, 444)],
            ["qcurve", 0, (443, 366)],
            ["line", 0, (443, 47)],
            ["line", 0, (515, 47)],
            ["line", 0, (515, 8)],
            [None, 0, (502, 0)],
            [None, 0, (462, -12)],
            ["qcurve", 0, (438, -12)],
            [None, 0, (395, -12)],
            [None, 0, (352, 33)],
            ["qcurve", 0, (352, 71)],
            ["line", 0, (352, 77)],
            ["line", 0, (348, 77)],
            [None, 0, (341, 60)],
            [None, 0, (318, 28)],
            [None, 0, (283, 3)],
            [None, 0, (233, -12)],
        ]
        assert contours[1] == [
            ["qcurve", 0, (238, 50)],  # was "move"
            [None, 0, (284, 50)],
            [None, 0, (347, 96)],
            ["qcurve", 0, (347, 145)],
            ["line", 0, (347, 239)],
            ["line", 0, (284, 239)],
            [None, 0, (206, 239)],
            [None, 0, (146, 190)],
            ["qcurve", 0, (146, 145)],
            ["line", 0, (146, 125)],
            [None, 0, (146, 87)],
            [None, 0, (195, 50)],
        ]
