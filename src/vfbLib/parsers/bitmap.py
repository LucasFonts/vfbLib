from __future__ import annotations

import logging

# from math import log2
# from struct import unpack
from typing import Any

from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class BaseBitmapParser(BaseParser):
    def parse_bitmap_data(self, w: int, h: int, datalen: int) -> dict[str, Any]:
        if datalen < 2:
            logger.error("parse_bitmap_data: Got datalen", datalen)
            raise ValueError

        flag = self.read_uint8()  # endianness?
        rows = []
        words = []
        uint32_per_column = (w + 16) // 16
        for _ in range(h):
            row = []
            for _ in range(uint32_per_column):
                word = self.read_uint16_be()
                words.append(word)
                row.append(word)
            rows.append(
                "".join(
                    [f"{r:016b}".replace("0", " ▕").replace("1", "█▉") for r in row]
                )
            )
        bitmap = {
            "flag": flag,
            "data": words,
            # "preview": rows,
        }
        return bitmap


class BackgroundBitmapParser(BaseBitmapParser):
    def _parse(self) -> dict[str, Any]:
        bitmap: dict[str, Any] = {}
        bitmap["origin"] = (self.read_value(), self.read_value())
        bitmap["size_units"] = (self.read_value(), self.read_value())
        w = self.read_value(signed=False)
        h = self.read_value(signed=False)
        bitmap["size_pixels"] = (w, h)
        datalen = self.read_value()
        bitmap["len"] = datalen
        bitmap["bitmap"] = self.parse_bitmap_data(w, h, datalen)
        return bitmap


class GlyphBitmapParser(BaseBitmapParser):
    def _parse(self) -> list[dict[str, Any]]:
        bitmaps: list[dict[str, Any]] = []
        num_bitmaps = self.read_value()
        for _ in range(num_bitmaps):
            bitmap: dict[str, Any] = {}
            bitmap["ppm"] = self.read_value()
            bitmap["origin"] = (self.read_value(), self.read_value())
            bitmap["adv"] = (self.read_value(), self.read_value())
            w = self.read_value(signed=False)
            h = self.read_value(signed=False)
            bitmap["size_pixels"] = (w, h)
            datalen = self.read_value()
            bitmap["len"] = datalen
            bitmap["bitmap"] = self.parse_bitmap_data(w, h, datalen)
            # bitmap["preview"] = pprint_bitmap(bitmap, invert=True)
            bitmaps.append(bitmap)
        return bitmaps
