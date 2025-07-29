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
        bitmap = BitmapDataDict(flag=0, data=[])
        pos = 0
        end_of_data = False
        bitmap["flag"] = self.read_uint8()
        pos += 1
        rows = []
        data = []
        values_per_row = (w + 16) // 16 * 2
        for _ in range(h):
            row = []
            for _ in range(values_per_row):
                i = self.read_uint8()
                pos += 1
                data.append(i)
                row.append(i)
                if pos >= datalen:
                    end_of_data = True
                    num_values = len(row)
                    if num_values < values_per_row:
                        # Row is too short, add zeroes
                        row.extend([0] * (values_per_row - num_values))
                    break

            rows.append(
                "".join([f"{r:08b}".replace("0", " ▕").replace("1", "█▉") for r in row])
            )
            if end_of_data:
                num_rows = len(rows)
                if num_rows < h:
                    # Height is too short, add empty rows
                    empty_row = " ▕" * values_per_row * 8
                    for _ in range(h - num_rows):
                        rows.append(empty_row)
                break
        bitmap["data"] = data
        if preview:
            if origin_top:
                bitmap["preview"] = [r for r in reversed(rows)]
            else:
                bitmap["preview"] = rows
            # for row in rows:
            #     print(row)
        return bitmap


class BackgroundBitmapParser(BaseBitmapParser):
    def _parse(self) -> BackgroundImageDict:
        bitmap = BackgroundImageDict(
            origin=(0, 0),
            size_units=(0, 0),
            size_pixels=(0, 0),
            bitmap=BitmapDataDict(flag=0, data=[]),
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
        # bitmap["len"] = datalen
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
                bitmap=BitmapDataDict(flag=0, data=[]),
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
            # bitmap["len"] = datalen
            bitmap["bitmap"] = self._parse_bitmap_data(w, h, datalen)
            bitmaps.append(bitmap)
        return bitmaps
