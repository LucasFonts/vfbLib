from __future__ import annotations

import logging

from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class MMKernPairParser(BaseParser):
    """
    A parser that reads the special-cased MM Kern Pair entry, which is apparently only
    written by FontLab 3.
    """

    def _parse(self) -> dict[str, int | list[int]]:
        index_1 = self.read_uint32()
        index_2 = self.read_uint32()
        pair = {"l": index_1, "r": index_2}
        values: list[int] = []
        for _ in range(self.master_count):
            values.append(self.read_int16())
        pair["values"] = values
        return pair
