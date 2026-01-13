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
                page_name=self.read_str_with_len(),
            )
            values.append(cmap)
        return values
