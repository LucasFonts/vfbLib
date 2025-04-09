from __future__ import annotations

from typing import Any

from vfbLib.compilers.base import BaseCompiler


class FloatListCompiler(BaseCompiler):
    """
    A compiler that compiles a list of floats.
    """

    def _compile(self, data: Any) -> None:
        self.write_floats(data)


class DoubleListCompiler(FloatListCompiler):
    """
    A compiler that compiles a list of doubles.
    """

    def _compile(self, data: Any) -> None:
        self.write_doubles(data)


class Int16Compiler(BaseCompiler):
    """
    A compiler that compiles UInt16 data.
    """

    def _compile(self, data: Any) -> None:
        self.write_uint16(data)
