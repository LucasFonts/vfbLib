from __future__ import annotations

import logging

from vfbLib import ExpandKernOptions, TTAutoHintOptions, export_options, font_options
from vfbLib.helpers import binaryToIntList
from vfbLib.parsers.base import BaseParser, EncodedKeyValuesParser
from vfbLib.typing import FontOptionsDict

logger = logging.getLogger(__name__)


class ExportOptionsParser(BaseParser):
    """
    A parser that reads data a bit field representing export options.
    """

    def _parse(self) -> list[str | int]:
        val = self.read_uint16()
        bits = binaryToIntList(val)
        options = [export_options.get(i, i) for i in bits]
        return options


class FontOptionsParser(EncodedKeyValuesParser):
    def _parse(self) -> FontOptionsDict:
        options = FontOptionsDict()
        for d in super()._parse():
            assert len(d) == 1
            k, v = tuple(d.items())[0]
            options[font_options.get(k, str(k))] = v

        # Post-process some entries

        for key in ("auto_hinting_h_ratio", "auto_hinting_v_ratio"):
            if key in options:
                options[key] /= 10_000

        if "autohinting_options" in options:
            val = options["autohinting_options"]
            options["autohinting_options"] = {
                "single_link_attachment_precision": val
                & TTAutoHintOptions.single_link_attachment_precision,
                "generate_triple_hints": int(
                    bool(val & TTAutoHintOptions.generate_triple_hints)
                ),
                "generate_delta_instructions": int(
                    bool(val & TTAutoHintOptions.generate_delta_instructions)
                ),
                "direct_links_to_center_of_the_glyph_where_possible": int(
                    bool(
                        val
                        & TTAutoHintOptions.direct_links_to_center_of_the_glyph_where_possible
                    )
                ),
                "interpolate_positions_of_cusp_points": int(
                    bool(val & TTAutoHintOptions.interpolate_positions_of_cusp_points)
                ),
                "interpolate_positions_of_double_links": int(
                    bool(val & TTAutoHintOptions.interpolate_positions_of_double_links)
                ),
                "add_link_to_rsb": int(bool(val & TTAutoHintOptions.add_link_to_rsb)),
            }

        if "expand_kern_flags" in options:
            val = options["expand_kern_flags"]
            options["expand_kern_flags"] = {
                "limit_action": int(bool(val & ExpandKernOptions.limit_action)),
                "limit_codepage": int(bool(val & ExpandKernOptions.limit_codepage)),
                "limit_cmap_10": int(bool(val & ExpandKernOptions.limit_cmap_10)),
                "limit_font_window": int(
                    bool(val & ExpandKernOptions.limit_font_window)
                ),
                "limit_count": int(bool(val & ExpandKernOptions.limit_count)),
                "limit_keep": int(bool(val & ExpandKernOptions.limit_keep)),
                "apply_to_assistance": int(
                    bool(val & ExpandKernOptions.apply_to_assistance)
                ),
            }

        return options
