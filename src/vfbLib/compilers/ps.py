from __future__ import annotations

from typing import Any

from vfbLib.compilers.base import BaseCompiler
from vfbLib.parsers.ps import global_options, glyph_options


class PostScriptInfoCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        font_matrix = data["font_matrix"]
        assert len(font_matrix) == 6
        self.write_doubles(data["font_matrix"])
        self.write_int32(data["force_bold"])
        for k, size in (
            ("blue_values", 14),
            ("other_blues", 10),
            ("family_blues", 14),
            ("family_other_blues", 10),
        ):
            values = data[k]
            assert len(values) == size
            for value in values:
                self.write_int32(value)
        self.write_double(data["blue_scale"])
        for k in (
            "blue_shift",
            "blue_fuzz",
            "std_hw",
            "std_vw",
        ):
            self.write_uint32(data[k])
        for k, size in (
            ("stem_snap_h", 12),
            ("stem_snap_v", 12),
        ):
            values = data[k]
            assert len(values) == size
            for value in values:
                self.write_uint32(value)
        for k in ("xMin", "yMin", "xMax", "yMax"):
            self.write_int16(data["bounding_box"][k])
        for k in (
            "adv_width_min",
            "adv_width_max",
            "adv_width_avg",
            "ascender",
            "descender",
            "x_height",
            "cap_height",
        ):
            self.write_int32(data[k])


class PostScriptGlobalHintingOptionsCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        value = 0
        for k, bit in global_options:
            if data.get(k, 0):
                value += 2**bit
        for bit in data.get("other", []):
            value += 2**bit
        self.write_uint16(value)


class PostScriptGlyphHintingOptionsCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        value = 0
        for k, bit in glyph_options:
            if data.get(k, 0):
                value += 2**bit
        for bit in data.get("other", []):
            value += 2**bit
        self.write_uint32(value)
