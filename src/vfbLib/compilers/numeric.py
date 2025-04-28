from __future__ import annotations

from struct import pack
from typing import Any

from vfbLib.compilers.base import BaseCompiler


class DoubleCompiler(BaseCompiler):
    """
    A compiler that compiles double-precision float data.
    """

    def _compile(self, data: Any) -> None:
        self.write_double(data)


class DoubleListCompiler(BaseCompiler):
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


class IntListCompiler(BaseCompiler):
    """
    A compiler that compiles a list of ints.
    """

    __size__ = 4

    def _compile(self, data: Any) -> None:
        for value in data:
            self.write_bytes(
                value.to_bytes(self.__size__, byteorder="little", signed=False)
            )


class PanoseCompiler(BaseCompiler):
    """
    A compiler that compiles PANOSE data.
    """

    def _compile(self, data: Any) -> None:
        b = pack("<10b", *data)
        self.write_bytes(b)


class SignedInt16Compiler(BaseCompiler):
    """
    A compiler that compiles Int16 data.
    """

    def _compile(self, data: Any) -> None:
        self.write_int16(data)


class SignedInt32Compiler(BaseCompiler):
    """
    A compiler that compiles Int32 data.
    """

    def _compile(self, data: Any) -> None:
        self.write_int32(data)


class UnicodeRangesCompiler(BaseCompiler):
    """
    A compiler that compiles the unicoderanges value into an uint64.
    """

    def _compile(self, data: list[int]) -> None:
        value = 0
        for b in data:
            value += 2**b
        self.write_bytes(value.to_bytes(16, byteorder="little", signed=False))
