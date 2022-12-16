from __future__ import annotations

import logging

from vfbLib.parsers import BaseParser
from vfbLib.parsers.value import read_encoded_value


logger = logging.getLogger(__name__)


class CustomCmapParser(BaseParser):
    """
    A parser that reads the custom CMAP settings.
    """

    @classmethod
    def _parse(cls):
        count = read_encoded_value(cls.stream)  # number of cmap records, not values
        values = {"values": []}
        for _ in range(count):
            cmap = {
                "language_id": read_encoded_value(cls.stream),
                "platform_id": read_encoded_value(cls.stream),
                "encoding_id": read_encoded_value(cls.stream),
                "format": read_encoded_value(cls.stream),
                "option": read_encoded_value(cls.stream),
                "records": [],
            }
            num_encodings = read_encoded_value(cls.stream)
            if num_encodings > 0:
                cmap["records"] = [cls.read_uint8() for _ in range(num_encodings)]
            values["values"].append(cmap)
        return values
