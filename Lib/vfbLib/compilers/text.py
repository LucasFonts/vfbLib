from __future__ import annotations
from typing import Any

from vfbLib.compilers.base import BaseCompiler


class StringCompiler(BaseCompiler):
    """
    A compiler that compiles string data.
    """

    def _compile(self, data: Any) -> None:
        self.write_str(data)
