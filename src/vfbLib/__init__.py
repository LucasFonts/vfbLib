from __future__ import annotations

from collections.abc import Sequence
from enum import IntEnum
from typing import Literal

# Used by guides and links
DIRECTIONS: Sequence[Literal["h", "v"]] = ("h", "v")

GLYPH_CONSTANT = (1, 9, 7, 1)

export_options = {
    0: "use_custom_opentype_export_options",
    1: "use_default_opentype_export_options",  # FIXME: Correct?
    2: "use_custom_cmap_encoding",
}

gdef_class_names = (
    "unassigned",  # 0
    "base",  # 1
    "ligature",  # 2
    "mark",  # 3
    "component",  # 4
)

replace_types = {
    0x01: "h",  # hintmask for hstem
    0x02: "v",  # hintmask for vstem
    0xFF: "r",  # Replacement point
    # FIXME: This seems to be the node index of the replacement
    # point. But sometimes it is negative, why?
}

mapping_modes = {
    0: "names_or_index",
    1: "unicode_ranges",
    3: "codepages",
}

font_options = {
    1: "fit_ascender",
    2: "fit_descender",
    3: "auto_metrics_left",
    4: "auto_metrics_right",
    5: "auto_metrics_close",
    6: "auto_hinting_min_h_len",
    7: "auto_hinting_min_v_len",
    8: "auto_hinting_min_h_width",
    9: "auto_hinting_min_v_width",
    10: "auto_hinting_max_h_width",
    11: "auto_hinting_max_v_width",
    12: "auto_hinting_h_ratio",  # when reading, divide by 10000
    13: "auto_hinting_v_ratio",  # when reading, divide by 10000
    14: "duplicate_place_x",
    15: "paste_place_x",
    16: "opentype_name_records",
    #    0 - "append_opentype_records_to_default_names"
    #    1 - "do_not_export_opentype_name_records"
    #    2 - "export_only_opentype_name_records"
    17: "codepage_for_cmap_1_0",
    #    0 - MacRoman (default)
    #    1 - Current codepage in font window
    #    2 - Windows 1250 Central European
    # Didn't bother to check from here on:
    #    3 - Windows 1251 Cyrillic
    #    4 - Windows 1252 Western (ANSI)
    #    ...
    #  153 - NeXT OS NextStep Multinational
    18: "dont_ignore_unicode_indexes",
    19: "head_bbox_savings",
    20: "autohinting_options",  # Bit field, see below
    21: "export_hinted_truetype_font",
    22: "autohint_unhinted_glyphs",
    23: "keep_existing_truetype_instructions",
    24: "export_visual_truetype_hints",
    25: "apply_bbox_savings",
    26: "auto_win_asc_desc",
    27: "add_characters",
    28: "export_embedded_bitmaps",
    29: "copy_hdmx_data_from_base_to_composite_glyph",
    30: "dont_automatically_reorder_glyphs",
    31: "export_ot",
    32: "export_volt",
    33: "write_kern_feature",
    34: "t1_terminal",
    35: "t1_pfm",
    36: "t1_afm",
    37: "t1_autohint",
    38: "t1_unicode",
    39: "optimize_align",
    40: "optimize_reduce",
    41: "t1_encoding",
    42: "ot_write_gdef",
    43: "t1_use_os2",
    44: "subrize",
    45: "t1_sort",
    46: "export_kern_table",
    47: "t1_fs_type",
    48: "expand_kern_flags",  # Bit field, see below
    49: "expand_kern_codepage",
    50: "expand_kern_count",
    51: "decompose",
    # 100: "end",
    114: "duplicate_place_y",
    115: "paste_place_y",
}


class TTAutoHintOptions(IntEnum):
    single_link_attachment_precision = 0x7
    generate_triple_hints = 0x100
    generate_delta_instructions = 0x200
    direct_links_to_center_of_the_glyph_where_possible = 0x400
    interpolate_positions_of_cusp_points = 0x800
    interpolate_positions_of_double_links = 0x1000
    add_link_to_rsb = 0x2000


class ExpandKernOptions(IntEnum):
    limit_action = 0x1
    limit_codepage = 0x2
    limit_cmap_10 = 0x4
    limit_font_window = 0x8
    limit_count = 0x10
    limit_keep = 0x20
    apply_to_assistance = 0x1000


ttinfo_names = {
    # 0x32: "end",
    0x33: "max_zones",
    0x34: "max_twilight_points",
    0x35: "max_storage",
    0x36: "max_function_defs",
    0x37: "max_instruction_defs",
    0x38: "max_stack_elements",
    0x39: "head_flags",  # tt_font_info_settings with head flags combined
    0x3A: "head_units_per_em",  # units_per_em, duplicate
    0x3B: "head_mac_style",
    0x3C: "head_lowest_rec_ppem",  # lowest_rec_ppem
    0x56: "head_creation",  # timestamp
    0x57: "head_creation2",  # head_modification? returned as second value in list
    0x3D: "head_font_direction_hint",  # font_direction_hint
    0x3E: "os2_us_weight_class",  # weight_class, duplicate
    0x3F: "os2_us_width_class",  # width_class, duplicate
    0x40: "os2_fs_type",  # embedding
    0x41: "os2_y_subscript_x_size",  # subscript_x_size
    0x42: "os2_y_subscript_y_size",  # subscript_y_size
    0x43: "os2_y_subscript_x_offset",  # subscript_x_offset
    0x44: "os2_y_subscript_y_offset",  # subscript_y_offset
    0x45: "os2_y_superscript_x_size",  # superscript_x_size
    0x46: "os2_y_superscript_y_size",  # superscript_y_size
    0x47: "os2_y_superscript_x_offset",  # superscript_x_offset
    0x48: "os2_y_superscript_y_offset",  # superscript_y_offset
    0x49: "os2_y_strikeout_size",  # strikeout_size
    0x4A: "os2_y_strikeout_position",  # strikeout_position
    0x4B: "os2_s_family_class",  # ibm_classification + subclass
    0x4C: "OpenTypeOS2Panose",
    0x4D: "os2_s_typo_ascender",  # OpenTypeOS2TypoAscender
    0x4E: "os2_s_typo_descender",  # OpenTypeOS2TypoDescender
    0x4F: "os2_s_typo_line_gap",  # OpenTypeOS2TypoLineGap
    0x50: "os2_fs_selection",
    0x51: "os2_us_win_ascent",  # OpenTypeOS2WinAscent
    0x52: "os2_us_win_descent",  # OpenTypeOS2WinDescent
    0x5C: "Average Width",
    0x53: "Hdmx PPMs 1",
    0x58: "Hdmx PPMs 2",
    # os2_ul_code_page_range1, os2_ul_code_page_range2:
    0x54: "Codepages",
    # Position unknown:
    0x59: "hhea_line_gap",
    0x5A: "hhea_ascender",
    0x5B: "hhea_descender",
}

tt_settings = {
    0: "use_custom_tt_values",
    1: "create_vdmx",
    2: "add_null_cr_space",
}


class TTFlags(IntEnum):
    use_custom_tt_values = 0x00010000
    create_vdmx = 0x00020000
    add_null_cr_space = 0x00040000
    create_hdmx = 0x00080000
    create_vmtx = 0x00100000
