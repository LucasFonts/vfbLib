from unittest import TestCase

from fontTools.misc.textTools import deHexStr, hexStr

from vfbLib.compilers.truetype import TrueTypeZoneDeltasCompiler, TrueTypeZonesCompiler
from vfbLib.parsers.truetype import TrueTypeZoneDeltasParser, TrueTypeZonesParser

expected_deltas = hexStr(
    deHexStr("958da7938da8838daa938dae838e9a838ea5838eab838eb8838fa7838fa983")
)
expected_zones = hexStr(
    deHexStr(
        "90f8049192696e665f746f70f89a979278686569676874f94e97946361706865696768"
        "74f9789792736c6173686573f9809793617363656e6465728e8b9793626173656c696e"
        "65fb5c979464657363656e646572f7de91927375705f626f74"
    )
)

# From IBMPlexSerif-Text.vfb
deltas = {
    2: {28: 8, 29: -8, 31: 8, 35: -8},
    3: {15: -8, 26: -8, 32: -8, 45: -8},
    4: {28: -8, 30: -8},
}

zones = {
    "ttZonesT": [
        {"position": 368, "value": 6, "name": "inf_top"},
        {"position": 518, "value": 12, "name": "xheight"},
        {"position": 698, "value": 12, "name": "capheight"},
        {"position": 740, "value": 12, "name": "slashes"},
        {"position": 748, "value": 12, "name": "ascender"},
    ],
    "ttZonesB": [
        {"position": 0, "value": 12, "name": "baseline"},
        {"position": -200, "value": 12, "name": "descender"},
        {"position": 330, "value": 6, "name": "sup_bot"},
    ],
}


class TrueTypeZoneDeltasCompilerTest(TestCase):
    def test_deltas(self):
        result = TrueTypeZoneDeltasCompiler().compile_hex(deltas)
        assert result == expected_deltas
        roundtrip = TrueTypeZoneDeltasParser().parse_hex(result)
        assert roundtrip == deltas

    def test_empty(self):
        result = TrueTypeZoneDeltasCompiler().compile_hex({})
        assert result == "8b"


class TrueTypeZonesCompilerTest(TestCase):
    def test_zones(self):
        result = TrueTypeZonesCompiler().compile_hex(zones)
        assert result == expected_zones
        roundtrip = TrueTypeZonesParser().parse_hex(result)
        assert roundtrip == zones

    def test_empty(self):
        result = TrueTypeZonesCompiler().compile_hex({})
        assert result == "8b8b"
