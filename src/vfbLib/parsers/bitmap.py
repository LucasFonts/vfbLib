from __future__ import annotations

import logging

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import BackgroundImageDict, BitmapDataDict, GlyphBitmapDict

logger = logging.getLogger(__name__)


class BaseBitmapParser(BaseParser):
    def _read_bitmap(self, datalen: int) -> list[list[int]]:
        # Read the bitmap data from the stream.
        # The returned value is in the run-length encoded representation.
        chunks: list[list[int]] = []
        bytes_remaining = datalen
        while bytes_remaining > 0:
            bytes_remaining -= 1
            # The next value specifies how many bytes to read and how to repeat them
            v = self.read_int8()
            chunk = [v]
            if v >= 0:
                # The next n bytes are actually stored in the data
                n = v + 1
                if n > bytes_remaining:
                    break

                for _ in range(n):
                    i = self.read_uint8()
                    chunk.append(i)
                bytes_remaining -= n
            else:
                # The next n bytes are identical, read only one byte and repeat it
                n = -v + 1
                if bytes_remaining < 1:
                    break

                i = self.read_uint8()
                chunk.append(i)
                bytes_remaining -= 1
            chunks.append(chunk)
        return chunks

    def _decode_bitmap(self, chunks: list[list[int]]) -> list[int]:
        # Decode from the run-length-encoded format
        decoded: list[int] = []
        for chunk in chunks:
            bytes_spec = chunk.pop(0)
            if bytes_spec >= 0:
                decoded.extend(chunk)
            else:
                num_values = -bytes_spec + 1
                decoded.extend(chunk * num_values)
        return decoded

    def _parse_bitmap_data(
        self,
        w: int,
        datalen: int,
        origin_top: bool = False,
        preview: bool = True,
    ) -> BitmapDataDict:
        rle_data = self._read_bitmap(datalen)
        data = self._decode_bitmap(rle_data)

        # For the "windows" platform, the bitmap must be inverted.
        if self.vfb is not None and self.vfb.writer_platform == "windows":
            data = [~b + 0x100 for b in data]

        # Split list into rows
        bytes_per_row = ((w + 15) // 16) * 2
        nice = [data[j : j + bytes_per_row] for j in range(0, len(data), bytes_per_row)]

        bitmap = BitmapDataDict(data=nice)

        # Generate an ASCII art preview
        if preview:
            rows = self._get_preview(bitmap["data"], w)
            if origin_top:
                bitmap["preview"] = [r for r in reversed(rows)]
            else:
                bitmap["preview"] = rows

        return bitmap

    def _get_preview(self, data: list[list[int]], payload_width: int) -> list[str]:
        # Add a block graphics bitmap preview to the decompiled data
        rows = []
        for row in data:
            preview_row = "".join(
                [f"{r:08b}".replace("0", " ▕").replace("1", "█▉") for r in row]
            )
            # Shorten row to the specified number of columns w
            preview_row = preview_row[: payload_width * 2]

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
        if not hasattr(self, "preview"):
            self.preview = True
        bitmap["bitmap"] = self._parse_bitmap_data(w, datalen, preview=self.preview)
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
            bitmap["bitmap"] = self._parse_bitmap_data(w, datalen)
            bitmaps.append(bitmap)
        return bitmaps
