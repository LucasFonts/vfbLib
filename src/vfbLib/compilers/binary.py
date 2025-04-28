from __future__ import annotations

from typing import Any

from vfbLib.compilers.base import BaseCompiler
from vfbLib.helpers import deHexStr


class BinaryTableCompiler(BaseCompiler):
    """
    A compiler that compiles binary table data.
    """

    def _compile(self, data: Any) -> None:
        self.write_str(data["tag"])  # FIXME: Add padding here?
        self.stream.write(deHexStr(data["data"]))
