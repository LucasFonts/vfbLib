from __future__ import annotations

import logging

from vfbLib.compilers.base import BaseCompiler

logger = logging.getLogger(__name__)


class FL3Type1410Compiler(BaseCompiler):
    def _compile(self, data: list[int]) -> None:
        for value in data:
            self.write_int16(value)
