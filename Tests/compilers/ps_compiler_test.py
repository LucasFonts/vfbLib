from unittest import TestCase

from vfbLib.compilers.ps import (
    PostScriptGlobalHintingOptionsCompiler,
    PostScriptGlyphHintingOptionsCompiler,
    PostScriptInfoCompiler,
)

psinfo_raw = {
    "font_matrix": [1.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    "force_bold": 0,
    "blue_values": [-12, 0, 368, 374, 518, 530, 698, 710, 748, 760, 758, 770, 0, 0],
    "other_blues": [-212, -200, 324, 330, 0, 0, 0, 0, 0, 0],
    "family_blues": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "family_other_blues": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "blue_scale": 0.039625,
    "blue_shift": 7,
    "blue_fuzz": 0,
    "std_hw": 50,
    "std_vw": 96,
    "stem_snap_h": [50, 54, 84, 67, 88, 0, 0, 0, 0, 0, 0, 0],
    "stem_snap_v": [96, 80, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "bounding_box": {"xMin": -260, "yMin": -254, "xMax": 1236, "yMax": 1128},
    "adv_width_min": 0,
    "adv_width_max": 0,
    "adv_width_avg": 0,
    "ascender": 780,
    "descender": -220,
    "x_height": 518,
    "cap_height": 698,
}

psinfo_exp = (
    # font_matrix
    "000000000000f03f"
    "0000000000000000"
    "0000000000000000"
    "000000000000f03f"
    "0000000000000000"
    "0000000000000000"
    # force_bold
    "00000000"
    # blue_values
    "f4ffffff"
    "00000000"
    "70010000"
    "76010000"
    "06020000"
    "12020000"
    "ba020000"
    "c6020000"
    "ec020000"
    "f8020000"
    "f6020000"
    "02030000"
    "00000000"
    "00000000"
    # other_blues
    "2cffffff"
    "38ffffff"
    "44010000"
    "4a010000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    # family_blues
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    # family_other_blues
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    # blue_scale
    "7d3f355eba49a43f"
    # blue_shift
    "07000000"
    # blue_fuzz
    "00000000"
    # std_hw
    "32000000"
    # std_vw
    "60000000"
    # stem_snap_h
    "32000000"
    "36000000"
    "54000000"
    "43000000"
    "58000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    # stem_snap_v
    "60000000"
    "50000000"
    "6e000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    "00000000"
    # bounding_box
    "fcfe"
    "02ff"
    "d404"
    "6804"
    # adv_width_min
    "00000000"
    # adv_width_max
    "00000000"
    # adv_width_avg
    "00000000"
    # ascender
    "0c030000"
    # descender
    "24ffffff"
    # x_height
    "06020000"
    # cap_height
    "ba020000"
)


class PostScriptGlobalHintingOptionsCompilerTest(TestCase):
    def test_nothing(self) -> None:
        result = PostScriptGlobalHintingOptionsCompiler().compile_hex(
            {"generate_flex": 0, "other": []}
        )
        assert result == "0000"

    def test_generate_flex(self) -> None:
        result = PostScriptGlobalHintingOptionsCompiler().compile_hex(
            {"generate_flex": 1, "other": []}
        )
        assert result == "0100"


class PostScriptGlyphHintingOptionsCompilerTest(TestCase):
    def test_nothing(self) -> None:
        result = PostScriptGlyphHintingOptionsCompiler().compile_hex(
            {
                "hint_replacement": 0,
                "horizontal_3_stem": 0,
                "vertical_3_stem": 0,
                "other": [],
            }
        )
        assert result == "00000000"

    def test_all(self) -> None:
        result = PostScriptGlyphHintingOptionsCompiler().compile_hex(
            {
                "hint_replacement": 1,
                "horizontal_3_stem": 1,
                "vertical_3_stem": 1,
                "other": [2],
            }
        )
        assert result == "040000e0"


class PostScriptInfoCompilerTest(TestCase):
    def test(self) -> None:
        result = PostScriptInfoCompiler().compile_hex(psinfo_raw)
        assert result == psinfo_exp
