from unittest import TestCase

from vfbLib.compilers.guides import GuidePropertiesCompiler, GuidesCompiler
from vfbLib.parsers.guides import GlobalGuidesParser, GuidePropertiesParser

raw_full = {
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

raw_partial = {
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
