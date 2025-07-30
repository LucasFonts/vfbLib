from __future__ import annotations

from collections.abc import Sequence
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

opentype_export_options = {
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
    20: "autohinting_options",
    #   bit  1 - 7: "single_link_attachment_precision"
    #   bit  8 - "generate_triple_hints"
    #   bit  9 - "generate_delta_instructions"
    #   bit 10 - "direct_links_to_center_of_the_glyph_where_possible"
    #   bit 11 - "interpolate_positions_of_cusp_points"
    #   bit 12 - "interpolate_positions_of_double_links"
    #   bit 14 - "add_link_to_rsb"
    21: "export_hinted_truetype_font",
    22: "autohint_unhinted_glyphs",
    23: "keep_existing_truetype_instructions",
    24: "export_visual_truetype_hints",
    28: "export_embedded_bitmaps",
    29: "copy_hdmx_data_from_base_to_composite_glyph",
    30: "dont_automatically_reorder_glyphs",
    46: "export_kern_table",
}

ttinfo_names = {
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
}

tt_settings = {
    0: "use_custom_tt_values",
    1: "create_vdmx",
    2: "add_null_cr_space",
}
