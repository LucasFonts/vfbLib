from unittest import TestCase

from pprint import pprint
from vfbLib.ufo.paths import get_master_glyph

# "a"
open_path = [
    {"type": "move", "flags": 11, "points": [[[92, 365]]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [[[364, 86], [92, 210], [214, 86]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[636, 365], [514, 86], [636, 210]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[364, 645], [636, 520], [514, 645]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[92, 365], [214, 645], [92, 520]]],
    },
    {"type": "move", "flags": 0, "points": [[[259, 347]]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [[[396, 490], [259, 426], [320, 490]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[534, 347], [472, 490], [534, 426]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[396, 205], [534, 268], [472, 205]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[259, 347], [320, 205], [259, 268]]],
    },
]

# "b"
closed_path = [
    {"type": "move", "flags": 3, "points": [[[92, 365]]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [[[364, 86], [92, 210], [214, 86]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[636, 365], [514, 86], [636, 210]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[364, 645], [636, 520], [514, 645]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[92, 365], [214, 645], [92, 520]]],
    },
    {"type": "move", "flags": 3, "points": [[[259, 347]]]},
    {
        "type": "curve",
        "flags": 3,
        "points": [[[396, 490], [259, 426], [320, 490]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[534, 347], [472, 490], [534, 426]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[396, 205], [534, 268], [472, 205]]],
    },
    {
        "type": "curve",
        "flags": 3,
        "points": [[[259, 347], [320, 205], [259, 268]]],
    },
]

# "c"
open_path_tt = [
    {"type": "move", "flags": 8, "points": [[[92, 365]]]},
    {"type": "qcurve", "flags": 0, "points": [[[92, 249]]]},
    {"type": "qcurve", "flags": 0, "points": [[[251, 86]]]},
    {"type": "line", "flags": 0, "points": [[[364, 86]]]},
    {"type": "qcurve", "flags": 0, "points": [[[477, 86]]]},
    {"type": "qcurve", "flags": 0, "points": [[[636, 249]]]},
    {"type": "line", "flags": 0, "points": [[[636, 365]]]},
    {"type": "qcurve", "flags": 0, "points": [[[636, 481]]]},
    {"type": "qcurve", "flags": 0, "points": [[[477, 645]]]},
    {"type": "line", "flags": 0, "points": [[[364, 645]]]},
    {"type": "qcurve", "flags": 0, "points": [[[251, 645]]]},
    {"type": "qcurve", "flags": 0, "points": [[[92, 481]]]},
    {"type": "line", "flags": 0, "points": [[[92, 365]]]},
    {"type": "move", "flags": 0, "points": [[[259, 347]]]},
    {"type": "qcurve", "flags": 0, "points": [[[259, 406]]]},
    {"type": "qcurve", "flags": 0, "points": [[[339, 490]]]},
    {"type": "line", "flags": 0, "points": [[[396, 490]]]},
    {"type": "qcurve", "flags": 0, "points": [[[453, 490]]]},
    {"type": "qcurve", "flags": 0, "points": [[[534, 406]]]},
    {"type": "line", "flags": 0, "points": [[[534, 347]]]},
    {"type": "qcurve", "flags": 0, "points": [[[534, 288]]]},
    {"type": "qcurve", "flags": 0, "points": [[[453, 205]]]},
    {"type": "line", "flags": 0, "points": [[[396, 205]]]},
    {"type": "qcurve", "flags": 0, "points": [[[339, 205]]]},
    {"type": "qcurve", "flags": 0, "points": [[[259, 288]]]},
]

# "d"
closed_path_tt = [
    {"type": "move", "flags": 0, "points": [[[92, 365]]]},
    {"type": "qcurve", "flags": 0, "points": [[[92, 249]]]},
    {"type": "qcurve", "flags": 0, "points": [[[251, 86]]]},
    {"type": "line", "flags": 0, "points": [[[364, 86]]]},
    {"type": "qcurve", "flags": 0, "points": [[[477, 86]]]},
    {"type": "qcurve", "flags": 0, "points": [[[636, 249]]]},
    {"type": "line", "flags": 0, "points": [[[636, 365]]]},
    {"type": "qcurve", "flags": 0, "points": [[[636, 481]]]},
    {"type": "qcurve", "flags": 0, "points": [[[477, 645]]]},
    {"type": "line", "flags": 0, "points": [[[364, 645]]]},
    {"type": "qcurve", "flags": 0, "points": [[[251, 645]]]},
    {"type": "qcurve", "flags": 0, "points": [[[92, 481]]]},
    {"type": "move", "flags": 0, "points": [[[259, 347]]]},
    {"type": "qcurve", "flags": 0, "points": [[[259, 406]]]},
    {"type": "qcurve", "flags": 0, "points": [[[339, 490]]]},
    {"type": "line", "flags": 0, "points": [[[396, 490]]]},
    {"type": "qcurve", "flags": 0, "points": [[[453, 490]]]},
    {"type": "qcurve", "flags": 0, "points": [[[534, 406]]]},
    {"type": "line", "flags": 0, "points": [[[534, 347]]]},
    {"type": "qcurve", "flags": 0, "points": [[[534, 288]]]},
    {"type": "qcurve", "flags": 0, "points": [[[453, 205]]]},
    {"type": "line", "flags": 0, "points": [[[396, 205]]]},
    {"type": "qcurve", "flags": 0, "points": [[[339, 205]]]},
    {"type": "qcurve", "flags": 0, "points": [[[259, 288]]]},
]

# "e"
closed_path_line = [
    {"type": "move", "flags": 0, "points": [[[172, 163]]]},
    {"type": "line", "flags": 0, "points": [[[395, 163]]]},
    {
        "type": "curve",
        "flags": 0,
        "points": [[[172, 612], [395, 360], [290, 612]]],
    },
    {"type": "move", "flags": 0, "points": [[[505, 152]]]},
    {"type": "line", "flags": 0, "points": [[[589, 152]]]},
    {"type": "qcurve", "flags": 0, "points": [[[598, 202]]]},
    {"type": "qcurve", "flags": 0, "points": [[[602, 310]]]},
    {"type": "qcurve", "flags": 0, "points": [[[594, 412]]]},
    {"type": "qcurve", "flags": 0, "points": [[[577, 503]]]},
    {"type": "qcurve", "flags": 0, "points": [[[552, 572]]]},
    {"type": "qcurve", "flags": 0, "points": [[[521, 612]]]},
    {"type": "line", "flags": 0, "points": [[[505, 612]]]},
    {"type": "move", "flags": 0, "points": [[[645, 113]]]},
    {"type": "line", "flags": 0, "points": [[[740, 113]]]},
    {"type": "line", "flags": 0, "points": [[[645, 603]]]},
]

# "f"
open_path_line = [
    {"type": "move", "flags": 8, "points": [[[172, 163]]]},
    {"type": "line", "flags": 0, "points": [[[395, 163]]]},
    {
        "type": "curve",
        "flags": 0,
        "points": [[[172, 612], [395, 360], [290, 612]]],
    },
    {"type": "line", "flags": 0, "points": [[[172, 163]]]},
    {"type": "move", "flags": 8, "points": [[[505, 152]]]},
    {"type": "line", "flags": 0, "points": [[[589, 152]]]},
    {"type": "qcurve", "flags": 0, "points": [[[598, 202]]]},
    {"type": "qcurve", "flags": 0, "points": [[[602, 310]]]},
    {"type": "qcurve", "flags": 0, "points": [[[594, 412]]]},
    {"type": "qcurve", "flags": 0, "points": [[[577, 503]]]},
    {"type": "qcurve", "flags": 0, "points": [[[552, 572]]]},
    {"type": "qcurve", "flags": 0, "points": [[[521, 612]]]},
    {"type": "line", "flags": 0, "points": [[[505, 612]]]},
    {"type": "line", "flags": 0, "points": [[[505, 152]]]},
    {"type": "move", "flags": 0, "points": [[[645, 113]]]},
    {"type": "line", "flags": 0, "points": [[[740, 113]]]},
    {"type": "line", "flags": 0, "points": [[[645, 603]]]},
]

# "a" from Plex Serif
complex_tt = [
    {"type": "move", "flags": 0, "points": [[[199, -12]]]},
    {"type": "qcurve", "flags": 0, "points": [[[124, -12]]]},
    {"type": "qcurve", "flags": 0, "points": [[[43, 64]]]},
    {"type": "line", "flags": 0, "points": [[[43, 130]]]},
    {"type": "qcurve", "flags": 0, "points": [[[43, 204]]]},
    {"type": "qcurve", "flags": 0, "points": [[[149, 282]]]},
    {"type": "line", "flags": 0, "points": [[[274, 282]]]},
    {"type": "line", "flags": 0, "points": [[[347, 282]]]},
    {"type": "line", "flags": 0, "points": [[[347, 355]]]},
    {"type": "qcurve", "flags": 0, "points": [[[347, 416]]]},
    {"type": "qcurve", "flags": 0, "points": [[[290, 480]]]},
    {"type": "line", "flags": 0, "points": [[[232, 480]]]},
    {"type": "qcurve", "flags": 0, "points": [[[207, 480]]]},
    {"type": "qcurve", "flags": 0, "points": [[[166, 472]]]},
    {"type": "line", "flags": 0, "points": [[[152, 464]]]},
    {"type": "line", "flags": 0, "points": [[[152, 462]]]},
    {"type": "qcurve", "flags": 0, "points": [[[163, 456]]]},
    {"type": "qcurve", "flags": 0, "points": [[[183, 432]]]},
    {"type": "line", "flags": 0, "points": [[[183, 410]]]},
    {"type": "qcurve", "flags": 0, "points": [[[183, 383]]]},
    {"type": "qcurve", "flags": 0, "points": [[[152, 352]]]},
    {"type": "line", "flags": 0, "points": [[[125, 352]]]},
    {"type": "qcurve", "flags": 0, "points": [[[99, 352]]]},
    {"type": "qcurve", "flags": 0, "points": [[[67, 384]]]},
    {"type": "line", "flags": 0, "points": [[[67, 413]]]},
    {"type": "qcurve", "flags": 0, "points": [[[67, 435]]]},
    {"type": "qcurve", "flags": 0, "points": [[[93, 477]]]},
    {"type": "qcurve", "flags": 0, "points": [[[143, 510]]]},
    {"type": "qcurve", "flags": 0, "points": [[[216, 530]]]},
    {"type": "line", "flags": 0, "points": [[[263, 530]]]},
    {"type": "qcurve", "flags": 0, "points": [[[351, 530]]]},
    {"type": "qcurve", "flags": 0, "points": [[[443, 444]]]},
    {"type": "line", "flags": 0, "points": [[[443, 366]]]},
    {"type": "line", "flags": 0, "points": [[[443, 47]]]},
    {"type": "line", "flags": 0, "points": [[[515, 47]]]},
    {"type": "line", "flags": 0, "points": [[[515, 8]]]},
    {"type": "qcurve", "flags": 0, "points": [[[502, 0]]]},
    {"type": "qcurve", "flags": 0, "points": [[[462, -12]]]},
    {"type": "line", "flags": 0, "points": [[[438, -12]]]},
    {"type": "qcurve", "flags": 0, "points": [[[395, -12]]]},
    {"type": "qcurve", "flags": 0, "points": [[[352, 33]]]},
    {"type": "line", "flags": 0, "points": [[[352, 71]]]},
    {"type": "line", "flags": 0, "points": [[[352, 77]]]},
    {"type": "line", "flags": 0, "points": [[[348, 77]]]},
    {"type": "qcurve", "flags": 0, "points": [[[341, 60]]]},
    {"type": "qcurve", "flags": 0, "points": [[[318, 28]]]},
    {"type": "qcurve", "flags": 0, "points": [[[283, 3]]]},
    {"type": "qcurve", "flags": 0, "points": [[[233, -12]]]},
    {"type": "move", "flags": 0, "points": [[[238, 50]]]},
    {"type": "qcurve", "flags": 0, "points": [[[284, 50]]]},
    {"type": "qcurve", "flags": 0, "points": [[[347, 96]]]},
    {"type": "line", "flags": 0, "points": [[[347, 145]]]},
    {"type": "line", "flags": 0, "points": [[[347, 239]]]},
    {"type": "line", "flags": 0, "points": [[[284, 239]]]},
    {"type": "qcurve", "flags": 0, "points": [[[206, 239]]]},
    {"type": "qcurve", "flags": 0, "points": [[[146, 190]]]},
    {"type": "line", "flags": 0, "points": [[[146, 145]]]},
    {"type": "line", "flags": 0, "points": [[[146, 125]]]},
    {"type": "qcurve", "flags": 0, "points": [[[146, 87]]]},
    {"type": "qcurve", "flags": 0, "points": [[[195, 50]]]},
]


class MMGlyph:
    def __init__(self, name, paths):
        self.name = name
        self.mm_nodes = paths


class PathsTest(TestCase):
    def test_closed_path(self):
        contours, components = get_master_glyph(
            MMGlyph("b", closed_path), [], 0
        )
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["curve", True, [92, 365]],
            [None, False, [92, 210]],
            [None, False, [214, 86]],
            ["curve", True, [364, 86]],
            [None, False, [514, 86]],
            [None, False, [636, 210]],
            ["curve", True, [636, 365]],
            [None, False, [636, 520]],
            [None, False, [514, 645]],
            ["curve", True, [364, 645]],
            [None, False, [214, 645]],
            [None, False, [92, 520]],
        ]
        assert contours[1] == [
            ["curve", True, [259, 347]],
            [None, False, [259, 426]],
            [None, False, [320, 490]],
            ["curve", True, [396, 490]],
            [None, False, [472, 490]],
            [None, False, [534, 426]],
            ["curve", True, [534, 347]],
            [None, False, [534, 268]],
            [None, False, [472, 205]],
            ["curve", True, [396, 205]],
            [None, False, [320, 205]],
            [None, False, [259, 268]],
        ]

    def test_open_path(self):
        contours, components = get_master_glyph(MMGlyph("a", open_path), [], 0)
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["move", True, [92, 365]],
            [None, False, [92, 210]],
            [None, False, [214, 86]],
            ["curve", True, [364, 86]],
            [None, False, [514, 86]],
            [None, False, [636, 210]],
            ["curve", True, [636, 365]],
            [None, False, [636, 520]],
            [None, False, [514, 645]],
            ["curve", True, [364, 645]],
            [None, False, [214, 645]],
            [None, False, [92, 520]],
            ["curve", True, [92, 365]],
        ]
        assert contours[1] == [
            ["curve", True, [259, 347]],
            [None, False, [259, 426]],
            [None, False, [320, 490]],
            ["curve", True, [396, 490]],
            [None, False, [472, 490]],
            [None, False, [534, 426]],
            ["curve", True, [534, 347]],
            [None, False, [534, 268]],
            [None, False, [472, 205]],
            ["curve", True, [396, 205]],
            [None, False, [320, 205]],
            [None, False, [259, 268]],
        ]

    def test_open_tt_path(self):
        contours, components = get_master_glyph(
            MMGlyph("c", open_path_tt), [], 0
        )
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["move", False, [92, 365]],
            [None, False, [92, 249]],
            [None, False, [251, 86]],
            ["qcurve", False, [364, 86]],
            [None, False, [477, 86]],
            [None, False, [636, 249]],
            ["qcurve", False, [636, 365]],
            [None, False, [636, 481]],
            [None, False, [477, 645]],
            ["qcurve", False, [364, 645]],
            [None, False, [251, 645]],
            [None, False, [92, 481]],
            ["qcurve", False, [92, 365]],
        ]
        assert contours[1] == [
            ["qcurve", False, [259, 347]],
            [None, False, [259, 406]],
            [None, False, [339, 490]],
            ["qcurve", False, [396, 490]],
            [None, False, [453, 490]],
            [None, False, [534, 406]],
            ["qcurve", False, [534, 347]],
            [None, False, [534, 288]],
            [None, False, [453, 205]],
            ["qcurve", False, [396, 205]],
            [None, False, [339, 205]],
            [None, False, [259, 288]],
        ]

    def test_closed_line_path(self):
        contours, components = get_master_glyph(
            MMGlyph("e", closed_path_line), [], 0
        )
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["line", False, [172, 163]],
            ["line", False, [395, 163]],
            [None, False, [395, 360]],
            [None, False, [290, 612]],
            ["curve", False, [172, 612]],
        ]
        assert contours[1] == [
            ["line", False, [505, 152]],
            ["line", False, [589, 152]],
            [None, False, [598, 202]],
            [None, False, [602, 310]],
            [None, False, [594, 412]],
            [None, False, [577, 503]],
            [None, False, [552, 572]],
            [None, False, [521, 612]],
            ["qcurve", False, [505, 612]],
        ]
        assert contours[2] == [
            ["line", False, [645, 113]],
            ["line", False, [740, 113]],
            ["line", False, [645, 603]],
        ]

    def test_open_line_path(self):
        contours, components = get_master_glyph(
            MMGlyph("f", open_path_line), [], 0
        )
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["move", False, [172, 163]],
            ["line", False, [395, 163]],
            [None, False, [395, 360]],
            [None, False, [290, 612]],
            ["curve", False, [172, 612]],
            ["line", False, [172, 163]],
        ]
        assert contours[1] == [
            ["move", False, [505, 152]],
            ["line", False, [589, 152]],
            [None, False, [598, 202]],
            [None, False, [602, 310]],
            [None, False, [594, 412]],
            [None, False, [577, 503]],
            [None, False, [552, 572]],
            [None, False, [521, 612]],
            ["qcurve", False, [505, 612]],
            ["line", False, [505, 152]],
        ]
        assert contours[2] == [
            ["line", False, [645, 113]],
            ["line", False, [740, 113]],
            ["line", False, [645, 603]],
        ]

    def test_complex_tt(self):
        contours, components = get_master_glyph(
            MMGlyph("a", complex_tt), [], 0
        )
        assert components == []
        pprint(contours)
        assert contours[0] == [
            ["qcurve", False, [199, -12]],  # was "move"
            [None, False, [124, -12]],
            [None, False, [43, 64]],
            ["qcurve", False, [43, 130]],
            [None, False, [43, 204]],
            [None, False, [149, 282]],
            ["qcurve", False, [274, 282]],
            ["line", False, [347, 282]],
            ["line", False, [347, 355]],
            [None, False, [347, 416]],
            [None, False, [290, 480]],
            ["qcurve", False, [232, 480]],
            [None, False, [207, 480]],
            [None, False, [166, 472]],
            ["qcurve", False, [152, 464]],
            ["line", False, [152, 462]],
            [None, False, [163, 456]],
            [None, False, [183, 432]],
            ["qcurve", False, [183, 410]],
            [None, False, [183, 383]],
            [None, False, [152, 352]],
            ["qcurve", False, [125, 352]],
            [None, False, [99, 352]],
            [None, False, [67, 384]],
            ["qcurve", False, [67, 413]],
            [None, False, [67, 435]],
            [None, False, [93, 477]],
            [None, False, [143, 510]],
            [None, False, [216, 530]],
            ["qcurve", False, [263, 530]],
            [None, False, [351, 530]],
            [None, False, [443, 444]],
            ["qcurve", False, [443, 366]],
            ["line", False, [443, 47]],
            ["line", False, [515, 47]],
            ["line", False, [515, 8]],
            [None, False, [502, 0]],
            [None, False, [462, -12]],
            ["qcurve", False, [438, -12]],
            [None, False, [395, -12]],
            [None, False, [352, 33]],
            ["qcurve", False, [352, 71]],
            ["line", False, [352, 77]],
            ["line", False, [348, 77]],
            [None, False, [341, 60]],
            [None, False, [318, 28]],
            [None, False, [283, 3]],
            [None, False, [233, -12]],
        ]
        assert contours[1] == [
            ["qcurve", False, [238, 50]],  # was "move"
            [None, False, [284, 50]],
            [None, False, [347, 96]],
            ["qcurve", False, [347, 145]],
            ["line", False, [347, 239]],
            ["line", False, [284, 239]],
            [None, False, [206, 239]],
            [None, False, [146, 190]],
            ["qcurve", False, [146, 145]],
            ["line", False, [146, 125]],
            [None, False, [146, 87]],
            [None, False, [195, 50]],
        ]
