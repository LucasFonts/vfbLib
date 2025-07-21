from __future__ import annotations

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import CustomCmap


class CustomCmapParser(BaseParser):
    """
    A parser that reads the custom CMAP settings.
    """

    def _parse(self) -> list[CustomCmap]:
        count = self.read_value()  # number of cmap records, not values
        values = []
        for _ in range(count):
            cmap = CustomCmap(
                language_id=self.read_value(),
                platform_id=self.read_value(),
                encoding_id=self.read_value(),
                format=self.read_value(),
                option=self.read_value(),
                records=[],
            )
            num_encodings = self.read_value()
            if num_encodings > 0:
                cmap["records"] = [self.read_uint8() for _ in range(num_encodings)]
            values.append(cmap)
        return values
