from __future__ import annotations

import logging

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import BackgroundImageDict, BitmapDataDict, GlyphBitmapDict

logger = logging.getLogger(__name__)


class BaseBitmapParser(BaseParser):
    def _parse_bitmap_data(
        self,
        w: int,
        h: int,
        datalen: int,
        origin_top: bool = False,
        preview: bool = True,
    ) -> BitmapDataDict:
        bitmap = BitmapDataDict(data=[])
        data = []
        bytes_per_row = ((w + 15) // 16) * 2
        bytes_remaining = datalen
        while bytes_remaining > 0:
            bytes_remaining -= 1
            # The next value specifies how many bytes to read and how to repeat them
            v = self.read_int8()
            if v >= 0:
                # The next n bytes are actually stored in the data
                n = v + 1
                if n > bytes_remaining:
                    break

                for _ in range(n):
                    i = self.read_uint8()
                    data.append(i)
                bytes_remaining -= n
            else:
                # The next n bytes are identical, read only one byte and repeat it
                n = -v + 1
                if bytes_remaining < 1:
                    break

                i = self.read_uint8()
                data.extend([i] * n)
                bytes_remaining -= 1

        bitmap["data"] = data
        if preview:
            rows = self._get_preview(data, w, h, bytes_per_row)
            if origin_top:
                bitmap["preview"] = [r for r in reversed(rows)]
            else:
                bitmap["preview"] = rows
        return bitmap

    def _get_preview(self, data, w: int, h: int, bytes_per_row: int) -> list[str]:
        # Add a block graphics bitmap preview to the decompiled data:
        rows = []
        pos = 0
        size = bytes_per_row * h
        for _ in range(h):
            row = []
            for _ in range(bytes_per_row):
                if pos >= size:
                    break

                row.append(data[pos])
                pos += 1

            preview_row = "".join(
                [f"{r:08b}".replace("0", " ▕").replace("1", "█▉") for r in row]
            )
            # Shorten row to the specified number of columns w
            preview_row = preview_row[: w * 2]

            rows.append(preview_row)
        return rows


class BackgroundBitmapParser(BaseBitmapParser):
    def _parse(self) -> BackgroundImageDict:
        bitmap = BackgroundImageDict(
            origin=(0, 0),
            size_units=(0, 0),
            size_pixels=(0, 0),
            bitmap=BitmapDataDict(data=[]),
        )
        bitmap["origin"] = (self.read_value(), self.read_value())
        bitmap["size_units"] = (
            self.read_value(signed=False),
            self.read_value(signed=False),
        )
        w = self.read_value(signed=False)
        h = self.read_value(signed=False)
        bitmap["size_pixels"] = (w, h)
        datalen = self.read_value(signed=False)
        bitmap["bitmap"] = self._parse_bitmap_data(w, h, datalen)
        return bitmap


class GlyphBitmapsParser(BaseBitmapParser):
    def _parse(self) -> list[GlyphBitmapDict]:
        bitmaps: list[GlyphBitmapDict] = []
        num_bitmaps = self.read_value(signed=False)
        for _ in range(num_bitmaps):
            bitmap = GlyphBitmapDict(
                ppm=0,
                origin=(0, 0),
                adv=(0, 0),
                size_pixels=(0, 0),
                bitmap=BitmapDataDict(data=[]),
            )
            bitmap["ppm"] = self.read_value(signed=False)
            bitmap["origin"] = (self.read_value(), self.read_value())
            bitmap["adv"] = (
                self.read_value(signed=False),
                self.read_value(signed=False),
            )
            w = self.read_value(signed=False)
            h = self.read_value(signed=False)
            bitmap["size_pixels"] = (w, h)
            datalen = self.read_value()
            bitmap["bitmap"] = self._parse_bitmap_data(w, h, datalen)
            bitmaps.append(bitmap)
        return bitmaps
