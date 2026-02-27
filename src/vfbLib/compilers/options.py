from __future__ import annotations

from vfbLib import ExpandKernOptions, TTAutoHintOptions, export_options, font_options
from vfbLib.compilers.base import BaseCompiler
from vfbLib.helpers import intListToBinary
from vfbLib.typing import FontOptionsDict


class ExportOptionsCompiler(BaseCompiler):
    def _compile(self, data: list[str]) -> None:
        rev = {v: k for k, v in export_options.items()}
        options = [rev[k] for k in data]
        self.write_uint16(intListToBinary(options))


class FontOptionsCompiler(BaseCompiler):
    def _compile(self, data: FontOptionsDict) -> None:
        rev = {v: k for k, v in font_options.items()}
        for k, v in data.items():
            raw_key = rev.get(k)
            assert raw_key is not None
            match k:
                case "auto_hinting_h_ratio" | "auto_hinting_v_ratio":
                    assert isinstance(v, float)
                    v = round(v * 10_000)
                case "autohinting_options":
                    assert isinstance(v, dict)
                    packed = v.get("single_link_attachment_precision", 7)
                    for subkey in (
                        "generate_triple_hints",
                        "generate_delta_instructions",
                        "direct_links_to_center_of_the_glyph_where_possible",
                        "interpolate_positions_of_cusp_points",
                        "interpolate_positions_of_double_links",
                        "add_link_to_rsb",
                    ):
                        packed += v.get(subkey, 0) * getattr(TTAutoHintOptions, subkey)
                    v = packed
                case "expand_kern_flags":
                    assert isinstance(v, dict)
                    packed = 0
                    for subkey in (
                        "limit_action",
                        "limit_codepage",
                        "limit_cmap_10",
                        "limit_font_window",
                        "limit_count",
                        "limit_keep",
                        "apply_to_assistance",
                    ):
                        packed += v.get(subkey, 0) * getattr(ExpandKernOptions, subkey)
                    v = packed
                case _:
                    pass
            self.write_uint8(raw_key)
            assert isinstance(v, int)
            self.write_value(v)
        self.write_uint8(0x64)
