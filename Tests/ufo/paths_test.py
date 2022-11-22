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
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[92, 249], [251, 86], [364, 86]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[477, 86], [636, 249], [636, 365]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[636, 481], [477, 645], [364, 645]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[251, 645], [92, 481], [92, 365]]],
    },
    {"type": "move", "flags": 0, "points": [[[259, 347]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[259, 406], [339, 490], [396, 490]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[453, 490], [534, 406], [534, 347]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[534, 288], [453, 205], [396, 205]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[339, 205], [259, 288], [259, 347]]],
    },
]

# "d"
closed_path_tt = [
    {"type": "move", "flags": 0, "points": [[[92, 365]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[92, 249], [251, 86], [364, 86]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[477, 86], [636, 249], [636, 365]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[636, 481], [477, 645], [364, 645]]],
    },
    {"type": "qcurve", "flags": 0, "points": [[[251, 645], [92, 481]]]},
    {"type": "move", "flags": 0, "points": [[[259, 347]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[259, 406], [339, 490], [396, 490]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[453, 490], [534, 406], [534, 347]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[534, 288], [453, 205], [396, 205]]],
    },
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
    {
        "type": "qcurve",
        "flags": 0,
        "points": [
            [
                [598, 202],
                [602, 310],
                [594, 412],
                [577, 503],
                [552, 572],
                [521, 612],
                [505, 612],
            ]
        ],
    },
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
    {
        "type": "qcurve",
        "flags": 0,
        "points": [
            [
                [598, 202],
                [602, 310],
                [594, 412],
                [577, 503],
                [552, 572],
                [521, 612],
                [505, 612],
            ]
        ],
    },
    {"type": "line", "flags": 0, "points": [[[505, 152]]]},
    {"type": "move", "flags": 0, "points": [[[645, 113]]]},
    {"type": "line", "flags": 0, "points": [[[740, 113]]]},
    {"type": "line", "flags": 0, "points": [[[645, 603]]]},
]

# "a" from Plex Serif
complex_tt = [
    {"type": "move", "flags": 0, "points": [[[199, -12]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[124, -12], [43, 64], [43, 130]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[43, 204], [149, 282], [274, 282]]],
    },
    {"type": "line", "flags": 0, "points": [[[347, 282]]]},
    {"type": "line", "flags": 0, "points": [[[347, 355]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[347, 416], [290, 480], [232, 480]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[207, 480], [166, 472], [152, 464]]],
    },
    {"type": "line", "flags": 0, "points": [[[152, 462]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[163, 456], [183, 432], [183, 410]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[183, 383], [152, 352], [125, 352]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[99, 352], [67, 384], [67, 413]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[67, 435], [93, 477], [143, 510], [216, 530], [263, 530]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[351, 530], [443, 444], [443, 366]]],
    },
    {"type": "line", "flags": 0, "points": [[[443, 47]]]},
    {"type": "line", "flags": 0, "points": [[[515, 47]]]},
    {"type": "line", "flags": 0, "points": [[[515, 8]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[502, 0], [462, -12], [438, -12]]],
    },
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[395, -12], [352, 33], [352, 71]]],
    },
    {"type": "line", "flags": 0, "points": [[[352, 77]]]},
    {"type": "line", "flags": 0, "points": [[[348, 77]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[341, 60], [318, 28], [283, 3], [233, -12]]],
    },
    {"type": "move", "flags": 0, "points": [[[238, 50]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[284, 50], [347, 96], [347, 145]]],
    },
    {"type": "line", "flags": 0, "points": [[[347, 239]]]},
    {"type": "line", "flags": 0, "points": [[[284, 239]]]},
    {
        "type": "qcurve",
        "flags": 0,
        "points": [[[206, 239], [146, 190], [146, 145]]],
    },
    {"type": "line", "flags": 0, "points": [[[146, 125]]]},
]


class MMGlyph:
    def __init__(self, name, paths):
        self.name = name
        self.mm_nodes = paths


class PathsTest(TestCase):
    # def test_closed_path(self):
    #     contours, components = get_master_glyph(
    #         MMGlyph("b", closed_path), [], 0
    #     )
    #     assert components == []
    #     pprint(contours)
    #     assert contours[0] == [
    #         ["curve", True, [92, 365]],
    #         ["curve", True, [[92, 210], [214, 86], [364, 86]]],
    #         ["curve", True, [[514, 86], [636, 210], [636, 365]]],
    #         ["curve", True, [[636, 520], [514, 645], [364, 645]]],
    #         ["curve", True, [[214, 645], [92, 520], [92, 365]]],
    #     ]
    #     assert contours[1] == [
    #         ["curve", 3, [259, 347]],
    #         [None, 3, [259, 426]],
    #         [None, 3, [320, 490]],
    #         ["curve", 3, [396, 490]],
    #         [None, 3, [472, 490]],
    #         [None, 3, [534, 426]],
    #         ["curve", 3, [534, 347]],
    #         [None, 3, [534, 268]],
    #         [None, 3, [472, 205]],
    #         ["curve", 3, [396, 205]],
    #         [None, 3, [320, 205]],
    #         [None, 3, [259, 268]],
    #     ]

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

    # def test_closed_line_path(self):
    #     contours, components = get_master_glyph(
    #         MMGlyph("e", closed_path_line), [], 0
    #     )
    #     assert components == []
    #     pprint(contours)
    #     assert contours[0] == [
    #         ["line", False, [172, 163]],
    #         ["line", False, [395, 163]],
    #         [None, False, [395, 360]],
    #         [None, False, [290, 612]],
    #         ["curve", False, [172, 612]],
    #     ]
    #     assert contours[1] == [
    #         ["line", False, [505, 152]],
    #         ["line", False, [589, 152]],
    #         [None, False, [598, 202]],
    #         [None, False, [602, 310]],
    #         [None, False, [594, 412]],
    #         [None, False, [577, 503]],
    #         [None, False, [552, 572]],
    #         [None, False, [521, 612]],
    #         ["qcurve", False, [505, 612]],
    #     ]
    #     assert contours[2] == [
    #         ["line", False, [645, 113]],
    #         ["line", False, [740, 113]],
    #         ["line", False, [645, 603]],
    #     ]

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

    # def test_complex_tt(self):
    #     contours, components = get_master_glyph(
    #         MMGlyph("a", complex_tt), [], 0
    #     )
    #     assert components == []
    #     pprint(contours)
    #     assert contours[0] == [
    #         ["qcurve", 0, (199, -12)],  # was "move"
    #         [None, 0, (124, -12)],
    #         [None, 0, [43, 64]],
    #         ["qcurve", 0, [43, 130]],
    #         [None, 0, [43, 204]],
    #         [None, 0, [149, 282]],
    #         ["qcurve", 0, [274, 282]],
    #         ["line", 0, [347, 282]],
    #         ["line", 0, [347, 355]],
    #         [None, 0, [347, 416]],
    #         [None, 0, [290, 480]],
    #         ["qcurve", 0, [232, 480]],
    #         [None, 0, [207, 480]],
    #         [None, 0, [166, 472]],
    #         ["qcurve", 0, [152, 464]],
    #         ["line", 0, [152, 462]],
    #         [None, 0, [163, 456]],
    #         [None, 0, [183, 432]],
    #         ["qcurve", 0, [183, 410]],
    #         [None, 0, [183, 383]],
    #         [None, 0, [152, 352]],
    #         ["qcurve", 0, [125, 352]],
    #         [None, 0, [99, 352]],
    #         [None, 0, [67, 384]],
    #         ["qcurve", 0, [67, 413]],
    #         [None, 0, [67, 435]],
    #         [None, 0, [93, 477]],
    #         [None, 0, [143, 510]],
    #         [None, 0, [216, 530]],
    #         ["qcurve", 0, [263, 530]],
    #         [None, 0, [351, 530]],
    #         [None, 0, [443, 444]],
    #         ["qcurve", 0, [443, 366]],
    #         ["line", 0, [443, 47]],
    #         ["line", 0, [515, 47]],
    #         ["line", 0, [515, 8]],
    #         [None, 0, [502, 0]],
    #         [None, 0, (462, -12)],
    #         ["qcurve", 0, (438, -12)],
    #         [None, 0, (395, -12)],
    #         [None, 0, [352, 33]],
    #         ["qcurve", 0, [352, 71]],
    #         ["line", 0, [352, 77]],
    #         ["line", 0, [348, 77]],
    #         [None, 0, [341, 60]],
    #         [None, 0, [318, 28]],
    #         [None, 0, [283, 3]],
    #         [None, 0, (233, -12)],
    #     ]
    #     assert contours[1] == [
    #         ["qcurve", 0, [238, 50]],  # was "move"
    #         [None, 0, [284, 50]],
    #         [None, 0, [347, 96]],
    #         ["qcurve", 0, [347, 145]],
    #         ["line", 0, [347, 239]],
    #         ["line", 0, [284, 239]],
    #         [None, 0, [206, 239]],
    #         [None, 0, [146, 190]],
    #         ["qcurve", 0, [146, 145]],
    #         ["line", 0, [146, 125]],
    #         [None, 0, [146, 87]],
    #         [None, 0, [195, 50]],
    #     ]
