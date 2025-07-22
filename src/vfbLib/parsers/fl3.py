from __future__ import annotations

import logging

from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class FL3Type1410Parser(BaseParser):
    """
    A parser that reads the special-cased 1410 entry, which is apparently only
    written by FontLab 3.
    """

    def _parse(self) -> list[int]:
        values = []
        for _ in range(5):
            values.append(self.read_int16())
        return values
