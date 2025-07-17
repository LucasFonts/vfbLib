from unittest import TestCase

from vfbLib.parsers.base import (
    EncodedValueListParser,
    OpenTypeKerningClassFlagsParser,
    OpenTypeMetricsClassFlagsParser,
)


class EncodedValueListParserTest(TestCase):
    def test_links_1(self):
        data = "8c 8d 89 8b"
        expected = [1, 2, -2, 0]
        result = EncodedValueListParser().parse_hex(data)
        assert result == expected


class OpenTypeClassFlagsParserTest(TestCase):
    def test_2_masters_kerning(self):
        # fmt: off
        data = (
            "8e"                # 3 entries follow

            # entry 1
            "92"                # 7 = string length
            "5f615f4c454654"    # _a_LEFT
            "fa94"              # 1024
            "8b"                # 0

            # entry 2
            "93"                # 8 = string length
            "5f615f5249474854"  # _a_RIGHT
            "ff00000800"        # 2048
            "8b"                # 0

            # entry 3
            "8d"                # 2 = string length
            "5f74"              # _t
            "ff00000c00"        # 3072
            "8b"                # 0
        )
        # fmt: on
        expected = {"_a_LEFT": (1024, 0), "_a_RIGHT": (2048, 0), "_t": (3072, 0)}
        result = OpenTypeKerningClassFlagsParser().parse_hex(data)
        assert result == expected

    def test_2_masters_metrics(self):
        # fmt: off
        data = (
            "8c"            # 1 entry follows

            # entry 1
            "91"            # 6 = string length
            "2e6d74727835"  # .mtrx5
            "8b"            # 0
            "ff00001401"    # 5121
            "8b"            # 0
        )
        # fmt: on
        expected = {".mtrx5": (0, 5121, 0)}

        result = OpenTypeMetricsClassFlagsParser().parse_hex(data)
        assert result == expected
