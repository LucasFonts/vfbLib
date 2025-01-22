import logging

from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class CustomCmapParser(BaseParser):
    """
    A parser that reads the custom CMAP settings.
    """

    def _parse(self):
        count = self.read_value()  # number of cmap records, not values
        values = {"values": []}
        for _ in range(count):
            cmap = {
                "language_id": self.read_value(),
                "platform_id": self.read_value(),
                "encoding_id": self.read_value(),
                "format": self.read_value(),
                "option": self.read_value(),
                "records": [],
            }
            num_encodings = self.read_value()
            if num_encodings > 0:
                cmap["records"] = [self.read_uint8() for _ in range(num_encodings)]
            values["values"].append(cmap)
        return values
