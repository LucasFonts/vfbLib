from unittest import TestCase

from fontTools.misc.textTools import deHexStr, hexStr

from vfbLib.compilers.truetype import (
    GaspCompiler,
    TrueTypeInfoCompiler,
    TrueTypeStemPpems1Compiler,
    TrueTypeStemPpems23Compiler,
    TrueTypeStemPpemsCompiler,
    TrueTypeStemsCompiler,
    TrueTypeZoneDeltasCompiler,
    TrueTypeZonesCompiler,
    VdmxCompiler,
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


class GaspCompilerTest(TestCase):
    def test(self):
        expected_gasp = (
            # 8 10
            "08000a00"
            # 120 15
            "78000f00"
            # 65535 10
            "ffff0a00"
        )
        result = GaspCompiler().compile_hex(
            [
                {"maxPpem": 8, "flags": 10},
                {"maxPpem": 120, "flags": 15},
                {"maxPpem": 65535, "flags": 10},
            ]
        )
        assert result == expected_gasp


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
                "head_creation2": 0,
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


class TrueTypeStemPpems1CompilerTest(TestCase):
    def test_plex_sans(self):
        raw_stem_ppms = {
            "ttStemsV": [
                {"stem": 0, "round": {1: 0}},
                {"stem": 1, "round": {1: 0}},
                {"stem": 2, "round": {1: 0}},
                {"stem": 3, "round": {1: 0}},
                {"stem": 4, "round": {1: 0}},
                {"stem": 5, "round": {1: 0}},
                {"stem": 6, "round": {1: 0}},
                {"stem": 7, "round": {1: 0}},
                {"stem": 8, "round": {1: 0}},
                {"stem": 9, "round": {1: 0}},
                {"stem": 10, "round": {1: 0}},
                {"stem": 11, "round": {1: 0}},
                {"stem": 12, "round": {1: 0}},
                {"stem": 13, "round": {1: 0}},
                {"stem": 14, "round": {1: 0}},
            ],
            "ttStemsH": [
                {"stem": 0, "round": {1: 0}},
                {"stem": 1, "round": {1: 0}},
            ],
        }
        expected_stem_ppms = "8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b8b"
        result = TrueTypeStemPpems1Compiler().compile_hex(raw_stem_ppms)
        assert result == expected_stem_ppms


class TrueTypeStemPpems23CompilerTest(TestCase):
    def test_plex_sans(self):
        raw_stem_ppms = {
            "ttStemsV": [
                {"stem": 0, "round": {2: 14, 3: 21}},
                {"stem": 1, "round": {2: 21, 3: 43}},
                {"stem": 2, "round": {2: 21, 3: 31}},
                {"stem": 3, "round": {2: 21, 3: 31}},
                {"stem": 4, "round": {2: 21, 3: 31}},
                {"stem": 5, "round": {2: 21, 3: 31}},
                {"stem": 6, "round": {2: 16, 3: 26}},
            ],
            "ttStemsH": [
                {"stem": 0, "round": {2: 19, 3: 21}},
                {"stem": 1, "round": {2: 19, 3: 31}},
                {"stem": 2, "round": {2: 19, 3: 31}},
                {"stem": 3, "round": {2: 19, 3: 31}},
                {"stem": 4, "round": {2: 19, 3: 31}},
                {"stem": 5, "round": {2: 19, 3: 31}},
            ],
        }
        expected_stem_ppms = (
            "92"  # 7
            "99a0"
            "a0b6"
            "a0aa"
            "a0aa"
            "a0aa"
            "a0aa"
            "9ba5"
            "91"  # 6
            "9ea0"
            "9eaa"
            "9eaa"
            "9eaa"
            "9eaa"
            "9eaa"
        )
        result = TrueTypeStemPpems23Compiler().compile_hex(raw_stem_ppms)
        assert result == expected_stem_ppms


class TrueTypeStemPpemsCompilerTest(TestCase):
    def test_plex_sans(self):
        raw_stem_ppms = {
            "ttStemsV": [
                {"stem": 0, "round": {2: 21, 3: 35, 4: 46, 5: 59}},
                {"stem": 1, "round": {2: 21, 3: 35, 4: 42, 5: 54}},
                {"stem": 2, "round": {2: 17, 3: 31, 4: 43, 5: 55}},
                {"stem": 3, "round": {2: 25, 3: 41, 4: 58, 5: 74}},
                {"stem": 4, "round": {2: 17, 3: 28, 4: 45, 5: 57}},
                {"stem": 5, "round": {2: 17, 3: 27, 4: 37, 5: 50}},
                {"stem": 6, "round": {2: 19, 3: 35, 4: 50, 5: 65}},
                {"stem": 7, "round": {2: 14, 3: 24, 4: 33, 5: 42}},
                {"stem": 8, "round": {2: 20, 3: 34, 4: 47, 5: 60}},
                {"stem": 9, "round": {2: 30, 3: 50, 4: 70, 5: 90}},
                {"stem": 10, "round": {2: 38, 3: 63, 4: 88, 5: 113}},
                {"stem": 11, "round": {2: 10, 3: 17, 4: 24, 5: 32}},
                {"stem": 12, "round": {2: 27, 3: 41, 4: 57, 5: 73}},
                {"stem": 13, "round": {2: 17, 3: 27, 4: 37, 5: 50}},
                {"stem": 14, "round": {2: 10, 3: 17, 4: 24, 5: 30}},
            ],
            "ttStemsH": [
                {"stem": 0, "round": {2: 14, 3: 23, 4: 33, 5: 42}},
                {"stem": 1, "round": {2: 17, 3: 28, 4: 39, 5: 50}},
            ],
        }
        expected_stem_ppms = (
            "9a"  # 15
            "a0aeb9c6a0aeb5c19caab6c2a4b4c5d59ca7b8c49ca6b0bd9eaebdcc99a3acb59fadbac7a9bdd1e5b1cae3f705959ca3aba6b4c4d49ca6b0bd959ca3a98d99a2acb59ca7b2bd"
        )
        result = TrueTypeStemPpemsCompiler().compile_hex(raw_stem_ppms)
        assert result == expected_stem_ppms


class TrueTypeStemsCompilerTest(TestCase):
    def test_plex_sans(self):
        raw_stems = {
            "ttStemsV": [
                {"value": 77, "name": "currency_stroke", "round": {6: 72}},
                {"value": 84, "name": "currency_white", "round": {6: 66}},
                {"value": 83, "name": "diacritics_thick", "round": {6: 67}},
                {"value": 61, "name": "diacritics_thin", "round": {6: 91}},
                {"value": 79, "name": "g_eye", "round": {6: 70}},
                {"value": 91, "name": "lc-hstem", "round": {6: 60}},
                {"value": 70, "name": "lc-mid", "round": {6: 79}},
                {"value": 108, "name": "logo_ce", "round": {6: 51}},
                {"value": 75, "name": "logo_fcc", "round": {6: 74}},
                {"value": 50, "name": "ord_mid", "round": {6: 110}},
                {"value": 40, "name": "registered", "round": {6: 138}},
                {"value": 140, "name": "spur", "round": {6: 40}},
                {"value": 62, "name": "sup-hstem", "round": {6: 89}},
                {"value": 100, "name": "uc-hstem", "round": {6: 56}},
                {"value": 152, "name": "tosf_descender", "round": {6: 37}},
            ],
            "ttStemsH": [
                {"value": 109, "name": "X: 109", "round": {6: 51}},
                {"value": 91, "name": "X: 91", "round": {6: 61}},
            ],
        }
        expected_stems = (
            "9a"  # 15
            "d80f63757272656e63795f7374726f6b65d3"
            "df0e63757272656e63795f7768697465cd"
            "de10646961637269746963735f746869636bce"
            "c80f646961637269746963735f7468696ee6"
            "da05675f657965d1"
            "e6086c632d687374656dc7"
            "d1066c632d6d6964da"
            "f700076c6f676f5f6365be"
            "d6086c6f676f5f666363d5"
            "bd076f72645f6d6964f702"
            # 40
            "b30a72656769737465726564f71e"
            "f7200473707572b3"
            "c9097375702d687374656de4"
            "ef0875632d687374656dc3"
            "f72c0e746f73665f64657363656e646572b08d"
            "f70106583a20313039bee605583a203931c8"
        )
        result = TrueTypeStemsCompiler().compile_hex(raw_stems)
        assert result == expected_stems


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


class VdmxCompilerTest(TestCase):
    def test_empty(self):
        result = VdmxCompiler().compile_hex([])
        assert result == "8b"

    def test(self):
        exp_vdmx = (
            "f78c"
            "9394889494889595889696879797879898879999879a9a869b9b869c9c869d9d859e9e859f9f85"
            "a0a084a1a184a2a284a3a383a4a483a5a482a6a582a7a782a8a782a9a881aaa981abab80acac80adad80aead80afae7f"
            "b0af7fb1b07fb2b27eb3b27eb4b37eb5b47eb6b57db7b67db8b87cb9b87cbab97cbbba7cbcbb7bbdbc7bbebd7bbfbe7a"
            "c0bf7ac1c07ac2c179c3c279c4c478c5c578c6c578c7c678c8c777c9c877cac977cbca77cccb76cdcc76cecd75cfce75"
            "d0cf74d1d074d2d174d3d274d4d374d5d473d6d573d7d573d8d672d9d772dad871dbd971dcda71dddb71dedc70dfdd70"
            "e0de70e1df6fe2e06fe3e16fe4e26ee5e36ee6e46ee7e56ee8e66de9e76deae86debe96cecea6cedeb6beeec6befed6b"
            "f0ee6bf1ef6af2f06af3f16af4f269f5f369f6f469f700f568f701f668f702f70067f703f70167f704f70267f705f703"
            "67f706f70467f707f70566f708f70666f709f70766f70af70865f70bf70965f70cf70a64f70df70b64f70ef70c63f70f"
            "f70d64f710f70e63f711f70f63f712f70f63f713f71062f714f71162f715f71262f716f71361f717f71461f718f71560"
            "f719f71660f71af71760f71bf71860f71cf7195ff71df71a5ff71ef71b5ff71ff71c5ef720f71d5ef721f71e5ef722f7"
            "1f5df723f7205df724f7215df725f7225df726f7235cf727f7245cf728f7255cf729f7265bf72af7275bf72bf7285af7"
            "2cf7295af72df72a5af72ef72b59f72ff72c59f730f72d59f731f72e59f732f72f58f733f73058f734f73158f735f732"
            "57f736f73357f737f73457f738f73556f739f73656f73af73756f73bf73856f73cf73955f73df73a55f73ef73b55f73f"
            "f73c54f740f73d54f741f73e53f742f73f53f743f74053f744f74053f745f74152f746f74252f747f74352f748f74451"
            "f749f74551f74af74651f74bf74750f74cf74850f74df7494ff74ef74a4ff74ff74b4ff750f74c4ff751f74d4ff752f7"
            "4e4ef753f74f4ef754f7504ef755f7514df756f7524df757f7534cf758f7544cf759f7554cf75af7564cf75bf7574bf7"
            "5cf7584bf75df7594bf75ef75a4af75ff75b4af760f75c4af761f75d49f762f75e49f763f75f48f764f76048f765f761"
            "48f766f76248f767f76347f768f76447f769f76547f76af76646f76bf76746f76cf76846f76df76945f76ef76a45f76f"
            "f76b45f770f76c45f771f76d44f772f76e44f773f76f44f774f77043f775f77143f776f77142f777f77242f778f77342"
            "f779f77442f77af77541f77bf77641f77cf77741f77df77840f77ef77940f77ff77a40f780f77b3ff781f77c3ff782f7"
            "7d3ef783f77e3ef784f77f3ef785f7803ef786f7813ef787f7823df788f7833df789f7843df78af7853cf78bf7863cf7"
            "8cf7873bf78df7883bf78ef7893bf78ff78a3bf790f78b3af791f78c3af792f78d3af793f78e39"
        )
        result = VdmxCompiler().compile_hex(
            [
                {"pelHeight": 8, "max": 9, "min": -3},
                {"pelHeight": 9, "max": 9, "min": -3},
                {"pelHeight": 10, "max": 10, "min": -3},
                {"pelHeight": 11, "max": 11, "min": -4},
                {"pelHeight": 12, "max": 12, "min": -4},
                {"pelHeight": 13, "max": 13, "min": -4},
                {"pelHeight": 14, "max": 14, "min": -4},
                {"pelHeight": 15, "max": 15, "min": -5},
                {"pelHeight": 16, "max": 16, "min": -5},
                {"pelHeight": 17, "max": 17, "min": -5},
                {"pelHeight": 18, "max": 18, "min": -6},
                {"pelHeight": 19, "max": 19, "min": -6},
                {"pelHeight": 20, "max": 20, "min": -6},
                {"pelHeight": 21, "max": 21, "min": -7},
                {"pelHeight": 22, "max": 22, "min": -7},
                {"pelHeight": 23, "max": 23, "min": -7},
                {"pelHeight": 24, "max": 24, "min": -8},
                {"pelHeight": 25, "max": 25, "min": -8},
                {"pelHeight": 26, "max": 25, "min": -9},
                {"pelHeight": 27, "max": 26, "min": -9},
                {"pelHeight": 28, "max": 28, "min": -9},
                {"pelHeight": 29, "max": 28, "min": -9},
                {"pelHeight": 30, "max": 29, "min": -10},
                {"pelHeight": 31, "max": 30, "min": -10},
                {"pelHeight": 32, "max": 32, "min": -11},
                {"pelHeight": 33, "max": 33, "min": -11},
                {"pelHeight": 34, "max": 34, "min": -11},
                {"pelHeight": 35, "max": 34, "min": -11},
                {"pelHeight": 36, "max": 35, "min": -12},
                {"pelHeight": 37, "max": 36, "min": -12},
                {"pelHeight": 38, "max": 37, "min": -12},
                {"pelHeight": 39, "max": 39, "min": -13},
                {"pelHeight": 40, "max": 39, "min": -13},
                {"pelHeight": 41, "max": 40, "min": -13},
                {"pelHeight": 42, "max": 41, "min": -13},
                {"pelHeight": 43, "max": 42, "min": -14},
                {"pelHeight": 44, "max": 43, "min": -14},
                {"pelHeight": 45, "max": 45, "min": -15},
                {"pelHeight": 46, "max": 45, "min": -15},
                {"pelHeight": 47, "max": 46, "min": -15},
                {"pelHeight": 48, "max": 47, "min": -15},
                {"pelHeight": 49, "max": 48, "min": -16},
                {"pelHeight": 50, "max": 49, "min": -16},
                {"pelHeight": 51, "max": 50, "min": -16},
                {"pelHeight": 52, "max": 51, "min": -17},
                {"pelHeight": 53, "max": 52, "min": -17},
                {"pelHeight": 54, "max": 53, "min": -17},
                {"pelHeight": 55, "max": 54, "min": -18},
                {"pelHeight": 56, "max": 55, "min": -18},
                {"pelHeight": 57, "max": 57, "min": -19},
                {"pelHeight": 58, "max": 58, "min": -19},
                {"pelHeight": 59, "max": 58, "min": -19},
                {"pelHeight": 60, "max": 59, "min": -19},
                {"pelHeight": 61, "max": 60, "min": -20},
                {"pelHeight": 62, "max": 61, "min": -20},
                {"pelHeight": 63, "max": 62, "min": -20},
                {"pelHeight": 64, "max": 63, "min": -20},
                {"pelHeight": 65, "max": 64, "min": -21},
                {"pelHeight": 66, "max": 65, "min": -21},
                {"pelHeight": 67, "max": 66, "min": -22},
                {"pelHeight": 68, "max": 67, "min": -22},
                {"pelHeight": 69, "max": 68, "min": -23},
                {"pelHeight": 70, "max": 69, "min": -23},
                {"pelHeight": 71, "max": 70, "min": -23},
                {"pelHeight": 72, "max": 71, "min": -23},
                {"pelHeight": 73, "max": 72, "min": -23},
                {"pelHeight": 74, "max": 73, "min": -24},
                {"pelHeight": 75, "max": 74, "min": -24},
                {"pelHeight": 76, "max": 74, "min": -24},
                {"pelHeight": 77, "max": 75, "min": -25},
                {"pelHeight": 78, "max": 76, "min": -25},
                {"pelHeight": 79, "max": 77, "min": -26},
                {"pelHeight": 80, "max": 78, "min": -26},
                {"pelHeight": 81, "max": 79, "min": -26},
                {"pelHeight": 82, "max": 80, "min": -26},
                {"pelHeight": 83, "max": 81, "min": -27},
                {"pelHeight": 84, "max": 82, "min": -27},
                {"pelHeight": 85, "max": 83, "min": -27},
                {"pelHeight": 86, "max": 84, "min": -28},
                {"pelHeight": 87, "max": 85, "min": -28},
                {"pelHeight": 88, "max": 86, "min": -28},
                {"pelHeight": 89, "max": 87, "min": -29},
                {"pelHeight": 90, "max": 88, "min": -29},
                {"pelHeight": 91, "max": 89, "min": -29},
                {"pelHeight": 92, "max": 90, "min": -29},
                {"pelHeight": 93, "max": 91, "min": -30},
                {"pelHeight": 94, "max": 92, "min": -30},
                {"pelHeight": 95, "max": 93, "min": -30},
                {"pelHeight": 96, "max": 94, "min": -31},
                {"pelHeight": 97, "max": 95, "min": -31},
                {"pelHeight": 98, "max": 96, "min": -32},
                {"pelHeight": 99, "max": 97, "min": -32},
                {"pelHeight": 100, "max": 98, "min": -32},
                {"pelHeight": 101, "max": 99, "min": -32},
                {"pelHeight": 102, "max": 100, "min": -33},
                {"pelHeight": 103, "max": 101, "min": -33},
                {"pelHeight": 104, "max": 102, "min": -33},
                {"pelHeight": 105, "max": 103, "min": -34},
                {"pelHeight": 106, "max": 104, "min": -34},
                {"pelHeight": 107, "max": 105, "min": -34},
                {"pelHeight": 108, "max": 106, "min": -35},
                {"pelHeight": 109, "max": 107, "min": -35},
                {"pelHeight": 110, "max": 108, "min": -36},
                {"pelHeight": 111, "max": 109, "min": -36},
                {"pelHeight": 112, "max": 110, "min": -36},
                {"pelHeight": 113, "max": 111, "min": -36},
                {"pelHeight": 114, "max": 112, "min": -36},
                {"pelHeight": 115, "max": 113, "min": -37},
                {"pelHeight": 116, "max": 114, "min": -37},
                {"pelHeight": 117, "max": 115, "min": -37},
                {"pelHeight": 118, "max": 116, "min": -38},
                {"pelHeight": 119, "max": 117, "min": -38},
                {"pelHeight": 120, "max": 118, "min": -39},
                {"pelHeight": 121, "max": 119, "min": -39},
                {"pelHeight": 122, "max": 120, "min": -40},
                {"pelHeight": 123, "max": 121, "min": -39},
                {"pelHeight": 124, "max": 122, "min": -40},
                {"pelHeight": 125, "max": 123, "min": -40},
                {"pelHeight": 126, "max": 123, "min": -40},
                {"pelHeight": 127, "max": 124, "min": -41},
                {"pelHeight": 128, "max": 125, "min": -41},
                {"pelHeight": 129, "max": 126, "min": -41},
                {"pelHeight": 130, "max": 127, "min": -42},
                {"pelHeight": 131, "max": 128, "min": -42},
                {"pelHeight": 132, "max": 129, "min": -43},
                {"pelHeight": 133, "max": 130, "min": -43},
                {"pelHeight": 134, "max": 131, "min": -43},
                {"pelHeight": 135, "max": 132, "min": -43},
                {"pelHeight": 136, "max": 133, "min": -44},
                {"pelHeight": 137, "max": 134, "min": -44},
                {"pelHeight": 138, "max": 135, "min": -44},
                {"pelHeight": 139, "max": 136, "min": -45},
                {"pelHeight": 140, "max": 137, "min": -45},
                {"pelHeight": 141, "max": 138, "min": -45},
                {"pelHeight": 142, "max": 139, "min": -46},
                {"pelHeight": 143, "max": 140, "min": -46},
                {"pelHeight": 144, "max": 141, "min": -46},
                {"pelHeight": 145, "max": 142, "min": -46},
                {"pelHeight": 146, "max": 143, "min": -47},
                {"pelHeight": 147, "max": 144, "min": -47},
                {"pelHeight": 148, "max": 145, "min": -47},
                {"pelHeight": 149, "max": 146, "min": -48},
                {"pelHeight": 150, "max": 147, "min": -48},
                {"pelHeight": 151, "max": 148, "min": -49},
                {"pelHeight": 152, "max": 149, "min": -49},
                {"pelHeight": 153, "max": 150, "min": -49},
                {"pelHeight": 154, "max": 151, "min": -50},
                {"pelHeight": 155, "max": 152, "min": -50},
                {"pelHeight": 156, "max": 153, "min": -50},
                {"pelHeight": 157, "max": 154, "min": -50},
                {"pelHeight": 158, "max": 155, "min": -51},
                {"pelHeight": 159, "max": 156, "min": -51},
                {"pelHeight": 160, "max": 157, "min": -51},
                {"pelHeight": 161, "max": 158, "min": -52},
                {"pelHeight": 162, "max": 159, "min": -52},
                {"pelHeight": 163, "max": 160, "min": -52},
                {"pelHeight": 164, "max": 161, "min": -53},
                {"pelHeight": 165, "max": 162, "min": -53},
                {"pelHeight": 166, "max": 163, "min": -53},
                {"pelHeight": 167, "max": 164, "min": -53},
                {"pelHeight": 168, "max": 165, "min": -54},
                {"pelHeight": 169, "max": 166, "min": -54},
                {"pelHeight": 170, "max": 167, "min": -54},
                {"pelHeight": 171, "max": 168, "min": -55},
                {"pelHeight": 172, "max": 169, "min": -55},
                {"pelHeight": 173, "max": 170, "min": -56},
                {"pelHeight": 174, "max": 171, "min": -56},
                {"pelHeight": 175, "max": 172, "min": -56},
                {"pelHeight": 176, "max": 172, "min": -56},
                {"pelHeight": 177, "max": 173, "min": -57},
                {"pelHeight": 178, "max": 174, "min": -57},
                {"pelHeight": 179, "max": 175, "min": -57},
                {"pelHeight": 180, "max": 176, "min": -58},
                {"pelHeight": 181, "max": 177, "min": -58},
                {"pelHeight": 182, "max": 178, "min": -58},
                {"pelHeight": 183, "max": 179, "min": -59},
                {"pelHeight": 184, "max": 180, "min": -59},
                {"pelHeight": 185, "max": 181, "min": -60},
                {"pelHeight": 186, "max": 182, "min": -60},
                {"pelHeight": 187, "max": 183, "min": -60},
                {"pelHeight": 188, "max": 184, "min": -60},
                {"pelHeight": 189, "max": 185, "min": -60},
                {"pelHeight": 190, "max": 186, "min": -61},
                {"pelHeight": 191, "max": 187, "min": -61},
                {"pelHeight": 192, "max": 188, "min": -61},
                {"pelHeight": 193, "max": 189, "min": -62},
                {"pelHeight": 194, "max": 190, "min": -62},
                {"pelHeight": 195, "max": 191, "min": -63},
                {"pelHeight": 196, "max": 192, "min": -63},
                {"pelHeight": 197, "max": 193, "min": -63},
                {"pelHeight": 198, "max": 194, "min": -63},
                {"pelHeight": 199, "max": 195, "min": -64},
                {"pelHeight": 200, "max": 196, "min": -64},
                {"pelHeight": 201, "max": 197, "min": -64},
                {"pelHeight": 202, "max": 198, "min": -65},
                {"pelHeight": 203, "max": 199, "min": -65},
                {"pelHeight": 204, "max": 200, "min": -65},
                {"pelHeight": 205, "max": 201, "min": -66},
                {"pelHeight": 206, "max": 202, "min": -66},
                {"pelHeight": 207, "max": 203, "min": -67},
                {"pelHeight": 208, "max": 204, "min": -67},
                {"pelHeight": 209, "max": 205, "min": -67},
                {"pelHeight": 210, "max": 206, "min": -67},
                {"pelHeight": 211, "max": 207, "min": -68},
                {"pelHeight": 212, "max": 208, "min": -68},
                {"pelHeight": 213, "max": 209, "min": -68},
                {"pelHeight": 214, "max": 210, "min": -69},
                {"pelHeight": 215, "max": 211, "min": -69},
                {"pelHeight": 216, "max": 212, "min": -69},
                {"pelHeight": 217, "max": 213, "min": -70},
                {"pelHeight": 218, "max": 214, "min": -70},
                {"pelHeight": 219, "max": 215, "min": -70},
                {"pelHeight": 220, "max": 216, "min": -70},
                {"pelHeight": 221, "max": 217, "min": -71},
                {"pelHeight": 222, "max": 218, "min": -71},
                {"pelHeight": 223, "max": 219, "min": -71},
                {"pelHeight": 224, "max": 220, "min": -72},
                {"pelHeight": 225, "max": 221, "min": -72},
                {"pelHeight": 226, "max": 221, "min": -73},
                {"pelHeight": 227, "max": 222, "min": -73},
                {"pelHeight": 228, "max": 223, "min": -73},
                {"pelHeight": 229, "max": 224, "min": -73},
                {"pelHeight": 230, "max": 225, "min": -74},
                {"pelHeight": 231, "max": 226, "min": -74},
                {"pelHeight": 232, "max": 227, "min": -74},
                {"pelHeight": 233, "max": 228, "min": -75},
                {"pelHeight": 234, "max": 229, "min": -75},
                {"pelHeight": 235, "max": 230, "min": -75},
                {"pelHeight": 236, "max": 231, "min": -76},
                {"pelHeight": 237, "max": 232, "min": -76},
                {"pelHeight": 238, "max": 233, "min": -77},
                {"pelHeight": 239, "max": 234, "min": -77},
                {"pelHeight": 240, "max": 235, "min": -77},
                {"pelHeight": 241, "max": 236, "min": -77},
                {"pelHeight": 242, "max": 237, "min": -77},
                {"pelHeight": 243, "max": 238, "min": -78},
                {"pelHeight": 244, "max": 239, "min": -78},
                {"pelHeight": 245, "max": 240, "min": -78},
                {"pelHeight": 246, "max": 241, "min": -79},
                {"pelHeight": 247, "max": 242, "min": -79},
                {"pelHeight": 248, "max": 243, "min": -80},
                {"pelHeight": 249, "max": 244, "min": -80},
                {"pelHeight": 250, "max": 245, "min": -80},
                {"pelHeight": 251, "max": 246, "min": -80},
                {"pelHeight": 252, "max": 247, "min": -81},
                {"pelHeight": 253, "max": 248, "min": -81},
                {"pelHeight": 254, "max": 249, "min": -81},
                {"pelHeight": 255, "max": 250, "min": -82},
            ]
        )
        assert result == exp_vdmx
