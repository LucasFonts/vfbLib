from unittest import TestCase

from vfbLib.parsers.truetype import GaspParser

gasp_bin = (
    "08000200"  # 8 2
    "10000100"  # 16 1
    "ffff0300"  # 65535 3
)
gasp_raw = [
    {"maxPpem": 8, "flags": 2},
    {"maxPpem": 16, "flags": 1},
    {"maxPpem": 65535, "flags": 3},
]


class GaspParserTest(TestCase):
    def test(self) -> None:
        result = GaspParser().parse_hex(gasp_bin)
        assert result == gasp_raw
