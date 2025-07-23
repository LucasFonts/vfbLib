from unittest import TestCase

from vfbLib.compilers.base import (
    OpenTypeKerningClassFlagsCompiler,
    OpenTypeMetricsClassFlagsCompiler,
)


class OpenTypeKerningClassFlagsCompilerTest(TestCase):
    def test(self):
        expected = (
            "8e"  # 3: number of entries
            "92"  # 7: string length
            "5f615f4c454654"
            "fa94"  # 1024
            "8b"  # 0
            "93"  # 8
            "5f615f5249474854"
            "ff00000800"
            "8b"  # 0
            "8d"  # 2
            "5f74"
            "ff00000c00"
            "8b"  # 0
        )
        result = OpenTypeKerningClassFlagsCompiler().compile_hex(
            {"_a_LEFT": [1024, 0], "_a_RIGHT": [2048, 0], "_t": [3072, 0]}
        )
        assert result == expected


class OpenTypeMetricsClassFlagsCompilerTest(TestCase):
    def test(self):
        expected = (
            "8c"  # 1: number of entries
            "91"  # 6: string length
            "2e6d74727835"
            "8b"  # 0
            "ff00001401"
            "8b"  # 0
        )
        result = OpenTypeMetricsClassFlagsCompiler().compile_hex(
            {".mtrx5": [0, 5121, 0]}
        )
        assert result == expected
