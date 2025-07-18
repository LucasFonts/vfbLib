from unittest import TestCase

from fontTools.misc.textTools import deHexStr, hexStr

from vfbLib.compilers.truetype import (
    TrueTypeInfoCompiler,
    TrueTypeZoneDeltasCompiler,
    TrueTypeZonesCompiler,
)
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


class TrueTypeInfoCompilerTest(TestCase):
    def test(self):
        exp_info = (
            "338b"
            "348b"
            "358b"
            "368b"
            "378b"
            "388b"
            "398b"
            "3afa7c"
            "3b8b"
            "3c9456ff53a3a4ca578b"
            "3d8d"
            "3ef824"
            "3f90408b"
            "41f950"
            "42f91e"
            "438b"
            "44f720"
            "45f950"
            "46f91e"
            "478b"
            "48f871"
            "49bb"
            "4af7c4"
            "4b8b"
            "4c02060503050000000000"
            "4df9a0"
            "4efb70"
            "4ff7c0"
            "508b"
            "51fa95"
            "52f7a7"
            "5c8b"
            "53a2090a0b0c0d0f10111315181b1d2021252a2e32363a434b"
            "58a2090a0b0c0d0f10111315181b1d2021252a2e32363a434b"
            "54ff200001978b"
            "32"
        )
        result = TrueTypeInfoCompiler().compile_hex(
            {
                "max_zones": 0,
                "max_twilight_points": 0,
                "max_storage": 0,
                "max_function_defs": 0,
                "max_instruction_defs": 0,
                "max_stack_elements": 0,
                "head_flags": {"flags": [], "options": []},
                "head_units_per_em": 1000,
                "head_mac_style": 0,
                "head_lowest_rec_ppem": 9,
                "head_creation": 1403233482,
                "0x57": 0,
                "head_font_direction_hint": 2,
                "os2_us_weight_class": 400,
                "os2_us_width_class": 5,
                "os2_fs_type": 0,
                "os2_y_subscript_x_size": 700,
                "os2_y_subscript_y_size": 650,
                "os2_y_subscript_x_offset": 0,
                "os2_y_subscript_y_offset": 140,
                "os2_y_superscript_x_size": 700,
                "os2_y_superscript_y_size": 650,
                "os2_y_superscript_x_offset": 0,
                "os2_y_superscript_y_offset": 477,
                "os2_y_strikeout_size": 48,
                "os2_y_strikeout_position": 304,
                "os2_s_family_class": 0,
                "OpenTypeOS2Panose": [2, 6, 5, 3, 5, 0, 0, 0, 0, 0],
                "os2_s_typo_ascender": 780,
                "os2_s_typo_descender": -220,
                "os2_s_typo_line_gap": 300,
                "os2_fs_selection": 0,
                "os2_us_win_ascent": 1025,
                "os2_us_win_descent": 275,
                "Average Width": 0,
                "Hdmx PPMs 1": [
                    9,
                    10,
                    11,
                    12,
                    13,
                    15,
                    16,
                    17,
                    19,
                    21,
                    24,
                    27,
                    29,
                    32,
                    33,
                    37,
                    42,
                    46,
                    50,
                    54,
                    58,
                    67,
                    75,
                ],
                "Hdmx PPMs 2": [
                    9,
                    10,
                    11,
                    12,
                    13,
                    15,
                    16,
                    17,
                    19,
                    21,
                    24,
                    27,
                    29,
                    32,
                    33,
                    37,
                    42,
                    46,
                    50,
                    54,
                    58,
                    67,
                    75,
                ],
                "Codepages": {
                    "os2_ul_code_page_range1": 536871319,
                    "os2_ul_code_page_range2": 0,
                },
            }
        )
        assert result == exp_info


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
