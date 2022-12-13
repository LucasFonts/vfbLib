from __future__ import annotations

import logging

from typing import Any, Dict, List
from vfbLib.parsers import BaseParser, read_encoded_value



logger = logging.getLogger(__name__)


class GlyphBitmapParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[Dict[str, Any]]:
        s = cls.stream
        bitmaps: List[Dict[str, Any]] = []
        num_bitmaps = read_encoded_value(s)
        for _ in range(num_bitmaps):
            bitmap: Dict[str, Any] = {}
            bitmap["ppm"] = read_encoded_value(s)
            bitmap["origin"] = (
                read_encoded_value(s),
                read_encoded_value(s),
            )
            bitmap["adv"] = (
                read_encoded_value(s),
                read_encoded_value(s),
            )
            bitmap["size"] = (
                read_encoded_value(s),
                read_encoded_value(s),
            )
            datalen = read_encoded_value(s)
            bitmap["len"] = datalen
            data = []
            if datalen > 1:
                mask = cls.read_uint8()
                data.append(mask)
                for _ in range(datalen - 1):
                    b = cls.read_uint8()
                    data.append(b)
            bitmap["data"] = data
            bitmaps.append(bitmap)
        assert s.read() == b""
        return bitmaps
