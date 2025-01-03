import logging

from vfbLib.helpers import binaryToIntList
from vfbLib.parsers.base import BaseParser, EncodedKeyValuesParser

logger = logging.getLogger(__name__)


class ExportOptionsParser(BaseParser):
    """
    A parser that reads data a bit field representing export options.
    """

    def _parse(self):
        names = {
            0: "use_custom_opentype_export_options",
            # 1: "use_default_opentype_export_options",
            2: "use_custom_cmap_encoding",
        }
        val = self.read_uint16()
        bits = binaryToIntList(val)
        options = [names.get(i, str(i)) for i in bits]
        return options


class OpenTypeExportOptionsParser(EncodedKeyValuesParser):
    def _parse(self):
        names = {
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
        final = []
        for d in super()._parse():
            assert len(d) == 1
            k, v = list(d.items())[0]
            final.append({names.get(k, str(k)): v})
        return final
