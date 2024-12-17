from __future__ import annotations

from typing import Any

from vfbLib.compilers.base import BaseCompiler


class Int16Compiler(BaseCompiler):
    """
    A compiler that compiles UInt16 data.
    """

    def _compile(self, data: Any) -> None:
        self.write_uint16(data)
