from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vfbLib.compilers.base import BaseCompiler

if TYPE_CHECKING:
    from vfbLib.typing import BackgroundImageDict, BitmapDataDict, GlyphBitmapDict

logger = logging.getLogger(__name__)


class BaseBitmapCompiler(BaseCompiler):
    def _compile_bitmap_data(self, bitmap: BitmapDataDict) -> None:
        self.write_uint8(bitmap["flag"])
        for value in bitmap["data"]:
            self.write_uint8(value)


class BackgroundBitmapCompiler(BaseBitmapCompiler):
    def _compile(self, data: BackgroundImageDict) -> None:
        x, y = data["origin"]
        self.write_value(x)
        self.write_value(y)

        w, h = data["size_units"]
        self.write_value(w, signed=False)
        self.write_value(h, signed=False)

        w, h = data["size_pixels"]
        self.write_value(w, signed=False)
        self.write_value(h, signed=False)

        bitmap = data["bitmap"]
        self.write_value(1 + len(bitmap["data"]), signed=False)
        self._compile_bitmap_data(bitmap)


class GlyphBitmapsCompiler(BaseBitmapCompiler):
    def _compile(self, data: list[GlyphBitmapDict]) -> None:
        self.write_value(len(data), signed=False)
        for d in data:
            self.write_value(d["ppm"], signed=False)
            x, y = d["origin"]
            self.write_value(x)
            self.write_value(y)

            w, h = d["adv"]
            self.write_value(w, signed=False)
            self.write_value(h, signed=False)

            w, h = d["size_pixels"]
            self.write_value(w, signed=False)
            self.write_value(h, signed=False)

            bitmap = d["bitmap"]
            self.write_value(1 + len(bitmap["data"]), signed=False)
            self._compile_bitmap_data(bitmap)
