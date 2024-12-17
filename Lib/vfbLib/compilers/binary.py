from __future__ import annotations

from typing import Any

from fontTools.misc.textTools import deHexStr

from vfbLib.compilers.base import BaseCompiler


class BinaryTableCompiler(BaseCompiler):
    """
    A compiler that compiles binary table data.
    """

    def _compile(self, data: Any) -> None:
        self.write_str(data["tag"])  # FIXME: Add padding here?
        self.stream.write(deHexStr(data["data"]))
