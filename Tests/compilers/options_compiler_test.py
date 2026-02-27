from unittest import TestCase

from fontTools.misc.textTools import hexStr

from vfbLib.compilers.options import FontOptionsCompiler

font_options = {
    "fit_ascender": 1000,
    "fit_descender": -400,
    "auto_metrics_left": 30,
    "auto_metrics_right": 30,
    "auto_metrics_close": 10,
    "auto_hinting_min_h_len": 60,
    "auto_hinting_min_v_len": 60,
    "auto_hinting_min_h_width": 20,
    "auto_hinting_min_v_width": 20,
    "auto_hinting_max_h_width": 250,
    "auto_hinting_max_v_width": 250,
    "auto_hinting_h_ratio": 2.0,
    "auto_hinting_v_ratio": 2.0,
    "duplicate_place_x": 100,
    "duplicate_place_y": 100,
    "paste_place_x": 0,
    "paste_place_y": 0,
    "opentype_name_records": 0,
    "codepage_for_cmap_1_0": 0,
    "dont_ignore_unicode_indexes": 1,
    "head_bbox_savings": 64,
    "autohinting_options": {
        "single_link_attachment_precision": 7,
        "generate_triple_hints": 1,
        "generate_delta_instructions": 1,
        "direct_links_to_center_of_the_glyph_where_possible": 0,
        "interpolate_positions_of_cusp_points": 1,
        "interpolate_positions_of_double_links": 1,
        "add_link_to_rsb": 1,
    },
    "export_hinted_truetype_font": 1,
    "autohint_unhinted_glyphs": 0,
    "keep_existing_truetype_instructions": 0,
    "export_visual_truetype_hints": 1,
    "apply_bbox_savings": 1,
    "auto_win_asc_desc": 1,
    "add_characters": 1,
    "export_embedded_bitmaps": 0,
    "copy_hdmx_data_from_base_to_composite_glyph": 0,
    "dont_automatically_reorder_glyphs": 1,
    "subrize": 0,
    "decompose": 1,
    "export_ot": 1,
    "export_volt": 0,
    "write_kern_feature": 1,
    "ot_write_gdef": 1,
    "t1_terminal": 0,
    "t1_pfm": 1,
    "t1_afm": 1,
    "t1_fs_type": 1,
    "t1_autohint": 3,
    "t1_unicode": 1,
    "optimize_align": 2,
    "optimize_reduce": 2,
    "t1_encoding": 0,
    "t1_use_os2": 0,
    "t1_sort": 0,
    "export_kern_table": 1,
    "expand_kern_flags": {
        "limit_action": 0,
        "limit_codepage": 1,
        "limit_cmap_10": 1,
        "limit_font_window": 0,
        "limit_count": 1,
        "limit_keep": 0,
        "apply_to_assistance": 0,
    },
    "expand_kern_count": 2048,
    "expand_kern_codepage": -1,
}


font_options_hex = (
    "01fa7c02fc2403a904a9059506c707c7"
    "089f099f0af78e0bf78e0cff00004e20"
    "0dff00004e200eef72ef0f8b738b108b"
    "118b128c13cb14ff00003b07158c168b"
    "178b188c198c1a8c1b8c1c8b1d8b1e8c"
    "2c8b338c1f8c208b218c2a8c228b238c"
    "248c2f8c258e268c278d288d298b2b8b"
    "2d8b2e8c30a132ff00000800318a64"
)


class FontOptionsCompilerTest(TestCase):
    def test_compilation_504(self):
        b = FontOptionsCompiler().compile(font_options)
        assert hexStr(b) == font_options_hex
