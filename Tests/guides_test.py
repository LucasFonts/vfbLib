from unittest import TestCase

from vfbLib.compilers.guides import GuidePropertiesCompiler, GuidesCompiler
from vfbLib.parsers.guides import GlobalGuidesParser, GuidePropertiesParser
from vfbLib.typing import GuidePropertiesDict, MMGuidesDict

raw_full: GuidePropertiesDict = {
    "h": [
        {"index": 1, "color": "#c0c0c0", "name": "wtf"},
        {"index": 2, "color": "#80ff57", "name": "hjk"},
    ],
    "v": [{"index": 2, "color": "#008000", "name": "rsb"}],
}

bin_full = (
    "8c"  # 1: index
    "ff00c0c0c0"  # color
    "8e"  # 3
    "777466"
    "8d"  # 2: index
    "ff0057ff80"  # color
    "8e"  # 3
    "686a6b"
    "8b"  # 0  # end of horizontal guides
    "8d"  # 2: index
    "ff00008000"  # color
    "8e"  # 3
    "727362"
    "8b"  # 0  # end of vertical guides
)

raw_partial: GuidePropertiesDict = {
    "h": [
        {"index": 1, "color": "#c0c0c0", "name": "wtf"},
        {"index": 2, "color": "#80ff57", "name": "hjk"},
    ],
    "v": [{"index": 2, "name": "rsbwtf"}, {"index": 3, "color": "#ffff00"}],
}

bin_partial = (
    "8c"  # 1: index
    "ff00c0c0c0"  # color
    "8e"  # 3: length of name
    "777466"  # "wtf"
    "8d"  # 2: index
    "ff0057ff80"  # color
    "8e"  # 3: length of name
    "686a6b"  # "hjk"
    "8b"  # 0  # end of horizontal guides
    "8d"  # 2: index
    "8a"  # -1 = no color
    "91"  # 6: length of name
    "727362777466"  # "rsbwtf"
    "8e"  # 3
    "ff0000ffff"  # color
    "8b"  # 0: length of name
    "8b"
)


class GuidePropertiesCompilerTest(TestCase):
    def test_full(self):
        result = GuidePropertiesCompiler().compile_hex(raw_full)
        assert result == bin_full

    def test_partial(self):
        result = GuidePropertiesCompiler().compile_hex(raw_partial)
        assert result == bin_partial


class GuidePropertiesParserTest(TestCase):
    def test_full(self):
        result = GuidePropertiesParser().parse_hex(bin_full)
        assert result == raw_full

    def test_partial(self):
        result = GuidePropertiesParser().parse_hex(bin_partial)
        assert result == raw_partial


bin_guides = (
    "9e"  # 19 horizontal guides
    "fa688b"  # 980 0 (master 0)
    "fa688b"  # 980 0 (master 1)
    "fbd48b"  # -320 0 (master 0)
    "fbd48b"  # -320 0 (master 1)
    "f7be8b"
    "f7be8b"
    "f9ca8b"
    "f9cb8b"
    "f9c98b"
    "f9c38b"
    "f9378b"
    "f9378b"
    "f93f8b"
    "f9418b"
    "f8ba8b"
    "f8b78b"
    "f7f48b"
    "f7ec8b"
    "f7ec8b"
    "f7e28b"
    "f7528b"
    "f7528b"
    "f74d8b"
    "f74b8b"
    "388b"
    "388b"
    "fb238b"
    "fb108b"
    "fb2a8b"
    "fb168b"
    "fb348b"
    "fb1d8b"
    "f7c78b"
    "f7c78b"
    "f9b48b"
    "f9b68b"
    "f9ac8b"
    "f9ac8b"
    "8c"  # 1 vertical guide
    "fbb68b"  # -290 0 (master 0)
    "fbae8b"  # -282 0 (master 1)
)

raw_guides: MMGuidesDict = {
    "h": [
        [
            {"pos": 980, "angle": 0.0},
            {"pos": 980, "angle": 0.0},
        ],
        [
            {"pos": -320, "angle": 0.0},
            {"pos": -320, "angle": 0.0},
        ],
        [
            {"pos": 298, "angle": 0.0},
            {"pos": 298, "angle": 0.0},
        ],
        [
            {"pos": 822, "angle": 0.0},
            {"pos": 823, "angle": 0.0},
        ],
        [
            {"pos": 821, "angle": 0.0},
            {"pos": 815, "angle": 0.0},
        ],
        [
            {"pos": 675, "angle": 0.0},
            {"pos": 675, "angle": 0.0},
        ],
        [
            {"pos": 683, "angle": 0.0},
            {"pos": 685, "angle": 0.0},
        ],
        [
            {"pos": 550, "angle": 0.0},
            {"pos": 547, "angle": 0.0},
        ],
        [
            {"pos": 352, "angle": 0.0},
            {"pos": 344, "angle": 0.0},
        ],
        [
            {"pos": 344, "angle": 0.0},
            {"pos": 334, "angle": 0.0},
        ],
        [
            {"pos": 190, "angle": 0.0},
            {"pos": 190, "angle": 0.0},
        ],
        [
            {"pos": 185, "angle": 0.0},
            {"pos": 183, "angle": 0.0},
        ],
        [
            {"pos": -83, "angle": 0.0},
            {"pos": -83, "angle": 0.0},
        ],
        [
            {"pos": -143, "angle": 0.0},
            {"pos": -124, "angle": 0.0},
        ],
        [
            {"pos": -150, "angle": 0.0},
            {"pos": -130, "angle": 0.0},
        ],
        [
            {"pos": -160, "angle": 0.0},
            {"pos": -137, "angle": 0.0},
        ],
        [
            {"pos": 307, "angle": 0.0},
            {"pos": 307, "angle": 0.0},
        ],
        [
            {"pos": 800, "angle": 0.0},
            {"pos": 802, "angle": 0.0},
        ],
        [
            {"pos": 792, "angle": 0.0},
            {"pos": 792, "angle": 0.0},
        ],
    ],
    "v": [
        [
            {"pos": -290, "angle": 0.0},
            {"pos": -282, "angle": 0.0},
        ],
    ],
}

bin_guides_empty = "8b8b"

raw_guides_empty: MMGuidesDict = {"h": [], "v": []}

bin_glyph_2m = (
    "8d"  # 2: num_h_guides
    "f9828b"  # guide 1 master 1
    "f9828b"  # guide 1 master 2
    "f95a8b"  # guide 2 master 1
    "f95a8b"  # guide 2 master 2
    "8d"  # 2: num_v_guides
    "8b8b"  # guide 1 master 1
    "8b8b"  # guide 1 master 2
    "8b8b"  # guide 2 master 1
    "8b8b"  # guide 2 master 2
)
raw_glyph_2m: MMGuidesDict = {
    "h": [
        [{"pos": 750, "angle": 0.0}, {"pos": 750, "angle": 0.0}],
        [{"pos": 710, "angle": 0.0}, {"pos": 710, "angle": 0.0}],
    ],
    "v": [
        [{"pos": 0, "angle": 0.0}, {"pos": 0, "angle": 0.0}],
        [{"pos": 0, "angle": 0.0}, {"pos": 0, "angle": 0.0}],
    ],
}


class GlobalGuidesParserTest(TestCase):
    def test(self):
        result = GlobalGuidesParser().parse_hex(bin_guides, master_count=2)
        assert result == raw_guides

    def test_empty(self):
        result = GlobalGuidesParser().parse_hex(bin_guides_empty, master_count=2)
        assert result == raw_guides_empty

    def test_glyph_2m(self):
        result = GlobalGuidesParser().parse_hex(bin_glyph_2m, master_count=2)
        assert result == raw_glyph_2m


class GuidesCompilerTest(TestCase):
    def test(self):
        result = GuidesCompiler().compile_hex(raw_guides, master_count=2)
        assert result == bin_guides

    def test_empty(self):
        result = GuidesCompiler().compile_hex(raw_guides_empty, master_count=2)
        assert result == bin_guides_empty

    def test_glyph_2m(self):
        result = GuidesCompiler().compile_hex(raw_glyph_2m, master_count=2)
        assert result == bin_glyph_2m
