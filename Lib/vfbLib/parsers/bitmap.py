from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr, num2binary
# from math import log2
# from struct import unpack
from typing import Any, Dict, List
from vfbLib.parsers import BaseParser, read_encoded_value


logger = logging.getLogger(__name__)


def pprint_bitmap(bitmap, datalen) -> List[str]:
    # print(bitmap)
    mask = bitmap["mask"]
    data = bitmap["data"]
    b: List[str] = []
    for v in data:
        b.append(num2binary(v, bits=8).replace("0", "  ").replace("1", "██"))
    # i += 1
    # cols = bitmap["size"][0]
    # col_bytes = cols // 8
    # print("col_bytes", col_bytes)
    # rest = cols % 8
    # if rest > 0:
    #     col_bytes += 1
    # print(f"Cols: {cols}, bytes per line: {col_bytes}")
    # line = ""
    # for j in range(col_bytes):
    #     print("byte", j)
    #     if i < datalen:
    #         b = cls.read_uint8()
    #         i += 1
    #         pixels = num2binary(b, bits=8).replace("0", "  ").replace("1", "██")
    #         line += pixels
    #     else:
    #         print("Hit end of data")
    # print(f"|{line}|")
    # data.append(line)
    return b


class BaseBitmapParser(BaseParser):
    @classmethod
    def parse_bitmap_data(cls, datalen) -> Dict[str, Any]:
        bitmap: Dict[str, Any] = {}
        if datalen < 2:
            logger.error("parse_bitmap_data: Got datalen", datalen)
            raise ValueError
        
        rest = 2

        if datalen > 2:
            num_bytes = cls.read_uint8()
            # bitmap["num_bytes"] = num_bytes
            data = []
            for _ in range(num_bytes):
                data.append(cls.read_uint8())
            bitmap["bytes"] = data
            rest = datalen - num_bytes - 1

        extra = []
        for _ in range(rest):
            extra.append(cls.read_uint8())

        if extra:
            bitmap["extra"] = extra

        return bitmap


class BackgroundBitmapParser(BaseBitmapParser):
    @classmethod
    def _parse(cls) -> Dict[str, Any]:
        s = cls.stream
        bitmap: Dict[str, Any] = {}
        bitmap["origin"] = (read_encoded_value(s), read_encoded_value(s))
        bitmap["size_units"] = (read_encoded_value(s), read_encoded_value(s))
        bitmap["size_pixels"] = (read_encoded_value(s), read_encoded_value(s))
        datalen = read_encoded_value(s)
        # bitmap["len"] = datalen
        bitmap["data"] = cls.parse_bitmap_data(datalen)
        assert s.read() == b""
        return bitmap


class GlyphBitmapParser(BaseBitmapParser):
    @classmethod
    def _parse(cls) -> List[Dict[str, Any]]:
        s = cls.stream
        bitmaps: List[Dict[str, Any]] = []
        num_bitmaps = read_encoded_value(s)
        for _ in range(num_bitmaps):
            bitmap: Dict[str, Any] = {}
            bitmap["ppm"] = read_encoded_value(s)
            bitmap["origin"] = (read_encoded_value(s), read_encoded_value(s))
            bitmap["adv"] = (read_encoded_value(s), read_encoded_value(s))
            bitmap["size_pixels"] = (read_encoded_value(s), read_encoded_value(s))
            datalen = read_encoded_value(s)
            # bitmap["len"] = datalen
            bitmap["data"] = cls.parse_bitmap_data(datalen)
            bitmaps.append(bitmap)
        assert s.read() == b""
        return bitmaps
