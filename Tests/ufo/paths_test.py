from unittest import TestCase

from vfbLib.ufo.glyph import VfbToUfoGlyph
from vfbLib.ufo.paths import UfoMasterGlyph

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

# vfb2ufo optimizes away the last line with a closepath, but FL5 TTF export doesn't
# f from closepath.vfb:
no_closepath_tt = [
    # Contour 0
    {"type": "move", "flags": 0, "points": [[[127, 361]]]},
    {"type": "qcurve", "flags": 0, "points": [[[127, 633]]]},
    {"type": "line", "flags": 0, "points": [[[399, 633]]]},
    {"type": "qcurve", "flags": 0, "points": [[[671, 633]]]},
    {"type": "line", "flags": 0, "points": [[[671, 361]]]},
    {"type": "qcurve", "flags": 0, "points": [[[672, 89]]]},
    {"type": "line", "flags": 0, "points": [[[399, 89]]]},
    {"type": "line", "flags": 0, "points": [[[127, 361]]]},  # ***
    # Contour 1
    {"type": "move", "flags": 0, "points": [[[424, 192]]]},
    {"type": "qcurve", "flags": 0, "points": [[[585, 192]]]},
    {"type": "line", "flags": 0, "points": [[[585, 353]]]},
    {"type": "qcurve", "flags": 0, "points": [[[585, 514]]]},
    {"type": "line", "flags": 0, "points": [[[424, 514]]]},
    {"type": "qcurve", "flags": 0, "points": [[[263, 514]]]},
    {"type": "line", "flags": 0, "points": [[[263, 353]]]},
    {"type": "line", "flags": 0, "points": [[[424, 192]]]},  # ***
]


def MMGlyph(name, paths):
    g = VfbToUfoGlyph()
    g.name = name
    g.mm_nodes = paths
    g.point_labels = {}
    g.mm_metrics = [(1000, 0)]
    return g


def get_master_glyph(mm_glyph: VfbToUfoGlyph, glyph_order, master_index):
    m = UfoMasterGlyph(mm_glyph, glyph_order, master_index)
    m.build(minimal=True, include_ps_hints=False, encode_data_base64=False)
    return m.contours, m.components


class PathsTest(TestCase):
    def test_closed_path(self):
        contours, components = get_master_glyph(MMGlyph("b", closed_path), [], 0)
        assert components == []
        # pprint(contours)
        assert contours[0] == [
            ("curve", True, None, [92, 365]),
            (None, False, None, [92, 210]),
            (None, False, None, [214, 86]),
            ("curve", True, None, [364, 86]),
            (None, False, None, [514, 86]),
            (None, False, None, [636, 210]),
            ("curve", True, None, [636, 365]),
            (None, False, None, [636, 520]),
            (None, False, None, [514, 645]),
            ("curve", True, None, [364, 645]),
            (None, False, None, [214, 645]),
            (None, False, None, [92, 520]),
        ]
        assert contours[1] == [
            ("curve", True, None, [259, 347]),
            (None, False, None, [259, 426]),
            (None, False, None, [320, 490]),
            ("curve", True, None, [396, 490]),
            (None, False, None, [472, 490]),
            (None, False, None, [534, 426]),
            ("curve", True, None, [534, 347]),
            (None, False, None, [534, 268]),
            (None, False, None, [472, 205]),
            ("curve", True, None, [396, 205]),
            (None, False, None, [320, 205]),
            (None, False, None, [259, 268]),
        ]

    def test_open_path(self):
        contours, components = get_master_glyph(MMGlyph("a", open_path), [], 0)
        assert components == []
        # pprint(contours)
        assert contours[0] == [
            ("move", True, None, [92, 365]),
            (None, False, None, [92, 210]),
            (None, False, None, [214, 86]),
            ("curve", True, None, [364, 86]),
            (None, False, None, [514, 86]),
            (None, False, None, [636, 210]),
            ("curve", True, None, [636, 365]),
            (None, False, None, [636, 520]),
            (None, False, None, [514, 645]),
            ("curve", True, None, [364, 645]),
            (None, False, None, [214, 645]),
            (None, False, None, [92, 520]),
            ("curve", True, None, [92, 365]),
        ]
        assert contours[1] == [
            ("curve", True, None, [259, 347]),
            (None, False, None, [259, 426]),
            (None, False, None, [320, 490]),
            ("curve", True, None, [396, 490]),
            (None, False, None, [472, 490]),
            (None, False, None, [534, 426]),
            ("curve", True, None, [534, 347]),
            (None, False, None, [534, 268]),
            (None, False, None, [472, 205]),
            ("curve", True, None, [396, 205]),
            (None, False, None, [320, 205]),
            (None, False, None, [259, 268]),
        ]

    def test_open_tt_path(self):
        contours, components = get_master_glyph(MMGlyph("c", open_path_tt), [], 0)
        assert components == []
        # pprint(contours)
        assert contours[0] == [
            ("move", False, None, [92, 365]),
            (None, False, None, [92, 249]),
            (None, False, None, [251, 86]),
            ("qcurve", False, None, [364, 86]),
            (None, False, None, [477, 86]),
            (None, False, None, [636, 249]),
            ("qcurve", False, None, [636, 365]),
            (None, False, None, [636, 481]),
            (None, False, None, [477, 645]),
            ("qcurve", False, None, [364, 645]),
            (None, False, None, [251, 645]),
            (None, False, None, [92, 481]),
            ("qcurve", False, None, [92, 365]),
        ]
        assert contours[1] == [
            ("qcurve", False, None, [259, 347]),
            (None, False, None, [259, 406]),
            (None, False, None, [339, 490]),
            ("qcurve", False, None, [396, 490]),
            (None, False, None, [453, 490]),
            (None, False, None, [534, 406]),
            ("qcurve", False, None, [534, 347]),
            (None, False, None, [534, 288]),
            (None, False, None, [453, 205]),
            ("qcurve", False, None, [396, 205]),
            (None, False, None, [339, 205]),
            (None, False, None, [259, 288]),
        ]

    def test_closed_line_path(self):
        contours, components = get_master_glyph(MMGlyph("e", closed_path_line), [], 0)
        assert components == []
        # pprint(contours)
        assert contours[0] == [
            ("line", False, None, [172, 163]),
            ("line", False, None, [395, 163]),
            (None, False, None, [395, 360]),
            (None, False, None, [290, 612]),
            ("curve", False, None, [172, 612]),
        ]
        assert contours[1] == [
            ("line", False, None, [505, 152]),
            ("line", False, None, [589, 152]),
            (None, False, None, [598, 202]),
            (None, False, None, [602, 310]),
            (None, False, None, [594, 412]),
            (None, False, None, [577, 503]),
            (None, False, None, [552, 572]),
            (None, False, None, [521, 612]),
            ("qcurve", False, None, [505, 612]),
        ]
        assert contours[2] == [
            ("line", False, None, [645, 113]),
            ("line", False, None, [740, 113]),
            ("line", False, None, [645, 603]),
        ]

    def test_open_line_path(self):
        contours, components = get_master_glyph(MMGlyph("f", open_path_line), [], 0)
        assert components == []
        # pprint(contours)
        assert contours[0] == [
            ("move", False, None, [172, 163]),
            ("line", False, None, [395, 163]),
            (None, False, None, [395, 360]),
            (None, False, None, [290, 612]),
            ("curve", False, None, [172, 612]),
            ("line", False, None, [172, 163]),
        ]
        assert contours[1] == [
            ("move", False, None, [505, 152]),
            ("line", False, None, [589, 152]),
            (None, False, None, [598, 202]),
            (None, False, None, [602, 310]),
            (None, False, None, [594, 412]),
            (None, False, None, [577, 503]),
            (None, False, None, [552, 572]),
            (None, False, None, [521, 612]),
            ("qcurve", False, None, [505, 612]),
            ("line", False, None, [505, 152]),
        ]
        assert contours[2] == [
            ("line", False, None, [645, 113]),
            ("line", False, None, [740, 113]),
            ("line", False, None, [645, 603]),
        ]

    def test_complex_tt(self):
        contours, components = get_master_glyph(MMGlyph("a", complex_tt), [], 0)
        assert components == []
        # pprint(contours)
        assert contours[0] == [
            ("qcurve", False, None, [199, -12]),  # was "move"
            (None, False, None, [124, -12]),
            (None, False, None, [43, 64]),
            ("qcurve", False, None, [43, 130]),
            (None, False, None, [43, 204]),
            (None, False, None, [149, 282]),
            ("qcurve", False, None, [274, 282]),
            ("line", False, None, [347, 282]),
            ("line", False, None, [347, 355]),
            (None, False, None, [347, 416]),
            (None, False, None, [290, 480]),
            ("qcurve", False, None, [232, 480]),
            (None, False, None, [207, 480]),
            (None, False, None, [166, 472]),
            ("qcurve", False, None, [152, 464]),
            ("line", False, None, [152, 462]),
            (None, False, None, [163, 456]),
            (None, False, None, [183, 432]),
            ("qcurve", False, None, [183, 410]),
            (None, False, None, [183, 383]),
            (None, False, None, [152, 352]),
            ("qcurve", False, None, [125, 352]),
            (None, False, None, [99, 352]),
            (None, False, None, [67, 384]),
            ("qcurve", False, None, [67, 413]),
            (None, False, None, [67, 435]),
            (None, False, None, [93, 477]),
            (None, False, None, [143, 510]),
            (None, False, None, [216, 530]),
            ("qcurve", False, None, [263, 530]),
            (None, False, None, [351, 530]),
            (None, False, None, [443, 444]),
            ("qcurve", False, None, [443, 366]),
            ("line", False, None, [443, 47]),
            ("line", False, None, [515, 47]),
            ("line", False, None, [515, 8]),
            (None, False, None, [502, 0]),
            (None, False, None, [462, -12]),
            ("qcurve", False, None, [438, -12]),
            (None, False, None, [395, -12]),
            (None, False, None, [352, 33]),
            ("qcurve", False, None, [352, 71]),
            ("line", False, None, [352, 77]),
            ("line", False, None, [348, 77]),
            (None, False, None, [341, 60]),
            (None, False, None, [318, 28]),
            (None, False, None, [283, 3]),
            (None, False, None, [233, -12]),
        ]
        assert contours[1] == [
            ("qcurve", False, None, [238, 50]),  # was "move"
            (None, False, None, [284, 50]),
            (None, False, None, [347, 96]),
            ("qcurve", False, None, [347, 145]),
            ("line", False, None, [347, 239]),
            ("line", False, None, [284, 239]),
            (None, False, None, [206, 239]),
            (None, False, None, [146, 190]),
            ("qcurve", False, None, [146, 145]),
            ("line", False, None, [146, 125]),
            (None, False, None, [146, 87]),
            (None, False, None, [195, 50]),
        ]

    def test_no_closepath_tt(self):
        # A special case: vfb2ufo replaces the last line by a closepath,
        # but FL5 TrueType export doesn't, so the outline is incompatible between TTF
        # and UFO. We want to avoid that and be compatible to the TTF.
        contours, components = get_master_glyph(MMGlyph("a", no_closepath_tt), [], 0)
        assert components == []
        # pprint(contours)
        # The offending lines are commented out to make the test pass.
        # Affected contours should be fixed in the source VFB.
        assert contours[0] == [
            ("line", False, None, [127, 361]),
            (None, False, None, [127, 633]),
            ("qcurve", False, None, [399, 633]),
            (None, False, None, [671, 633]),
            ("qcurve", False, None, [671, 361]),
            (None, False, None, [672, 89]),
            ("qcurve", False, None, [399, 89]),
            ("line", False, None, [127, 361]),
        ]
        assert contours[1] == [
            ("line", False, None, [424, 192]),
            (None, False, None, [585, 192]),
            ("qcurve", False, None, [585, 353]),
            (None, False, None, [585, 514]),
            ("qcurve", False, None, [424, 514]),
            (None, False, None, [263, 514]),
            ("qcurve", False, None, [263, 353]),
            ("line", False, None, [424, 192]),
        ]
