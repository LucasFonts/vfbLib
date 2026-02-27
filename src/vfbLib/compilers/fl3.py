from __future__ import annotations

import logging

from vfbLib.compilers.base import BaseCompiler

logger = logging.getLogger(__name__)


class MMKernPairCompiler(BaseCompiler):
    def _compile(self, data: list[int]) -> None:
        for value in data:
            self.write_int16(value)
