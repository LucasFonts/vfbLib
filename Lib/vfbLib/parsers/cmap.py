import logging

from vfbLib.parsers.base import BaseParser, ReturnsDict
from vfbLib.parsers.value import read_encoded_value


logger = logging.getLogger(__name__)


class CustomCmapParser(ReturnsDict, BaseParser):
    """
    A parser that reads the custom CMAP settings.
    """

    def _parse(self):
        count = read_encoded_value(self.stream)  # number of cmap records, not values
        values = {"values": []}
        for _ in range(count):
            cmap = {
                "language_id": read_encoded_value(self.stream),
                "platform_id": read_encoded_value(self.stream),
                "encoding_id": read_encoded_value(self.stream),
                "format": read_encoded_value(self.stream),
                "option": read_encoded_value(self.stream),
                "records": [],
            }
            num_encodings = read_encoded_value(self.stream)
            if num_encodings > 0:
                cmap["records"] = [self.read_uint8() for _ in range(num_encodings)]
            values["values"].append(cmap)
        return values
