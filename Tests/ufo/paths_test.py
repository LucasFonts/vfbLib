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


class OpenPathGlyph:
    def __init__(self):
        self.mm_nodes = open_path


class OpenTTPathGlyph:
    def __init__(self):
        self.mm_nodes = open_path_tt


class ClosedPathGlyph:
    def __init__(self):
        self.mm_nodes = closed_path


class PathsTest(TestCase):
    def test_closed_path(self):
        contours, components = get_master_glyph(ClosedPathGlyph(), [], 0)
        assert components == []
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

    def test_open_path(self):
        contours, components = get_master_glyph(OpenPathGlyph(), [], 0)
        assert components == []
        assert contours[0] == [
            ["move", 11, (92, 365)],
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
            ["curve", 3, (92, 365)],
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

    def test_open_tt_path(self):
        contours, components = get_master_glyph(OpenTTPathGlyph(), [], 0)
        assert components == []
        pprint(contours[1])
        assert contours[0] == [
            ["move", 8, (92, 365)],
            [None, 0, (92, 249)],
            [None, 0, (251, 86)],
            ["qcurve", 0, (364, 86)],
            [None, 0, (477, 86)],
            [None, 0, (636, 249)],
            ["qcurve", 0, (636, 365)],
            [None, 0, (636, 481)],
            [None, 0, (477, 645)],
            ["qcurve", 0, (364, 645)],
            [None, 0, (251, 645)],
            [None, 0, (92, 481)],
            ["qcurve", 0, (92, 365)],
        ]
        assert contours[1] == [
            ["qcurve", 0, (259, 347)],
            [None, 0, (259, 406)],
            [None, 0, (339, 490)],
            ["qcurve", 0, (396, 490)],
            [None, 0, (453, 490)],
            [None, 0, (534, 406)],
            ["qcurve", 0, (534, 347)],
            [None, 0, (534, 288)],
            [None, 0, (453, 205)],
            ["qcurve", 0, (396, 205)],
            [None, 0, (339, 205)],
            [None, 0, (259, 288)],
        ]
