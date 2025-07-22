from __future__ import annotations

import logging
from struct import unpack

from vfbLib.helpers import binaryToIntList
from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class DoubleParser(BaseParser):
    """
    A parser that reads data as a double-size float.
    """

    def _parse(self):
        return self.read_double()


class FloatListParser(BaseParser):
    """
    A parser that reads data as a list of floats.
    """

    __size__ = 4
    __fmt__ = "f"

    def _parse(self):
        values = []
        for _ in range(self.stream.getbuffer().nbytes // self.__size__):
            values.extend(unpack(self.__fmt__, self.stream.read(self.__size__)))

        return values


class DoubleListParser(FloatListParser):
    """
    A parser that reads data as a list of doubles.
    """

    __size__ = 8
    __fmt__ = "d"


class Int16Parser(BaseParser):
    """
    A parser that reads data as UInt16.
    """

    def _parse(self):
        return self.read_uint16()


# class Int32Parser(BaseParser):
#     """
#     A parser that reads data as UInt32.
#     """

#     def _parse(self):
#         return self.read_uint32()


# class Int64Parser(BaseParser):
#     """
#     A parser that reads data as UInt64.
#     """

#     def _parse(self):
#         return int.from_bytes(self.stream.read(64), byteorder="little", signed=False)


class IntListParser(BaseParser):
    """
    A parser that reads data as a list of UInt16.
    """

    __size__ = 4

    def _parse(self):
        values = []
        for _ in range(self.stream.getbuffer().nbytes // self.__size__):
            values.append(
                int.from_bytes(
                    self.stream.read(self.__size__),
                    byteorder="little",
                    signed=False,
                )
            )
        return values


class PanoseParser(BaseParser):
    """
    A parser that reads data as an array representing PANOSE values.
    """

    def _parse(self):
        return list(unpack("<10b", self.stream.read()))


class SignedInt16Parser(BaseParser):
    """
    A parser that reads data as signed int16.
    """

    def _parse(self):
        return self.read_int16()


class SignedInt32Parser(BaseParser):
    """
    A parser that reads data as signed int32.
    """

    def _parse(self):
        # return int.from_bytes(self.stream.read(), byteorder="little", signed=True)
        return self.read_int32()


class UnicodeRangesParser(BaseParser):
    """
    A parser that reads data as uint64 and returns it as a list of bit numbers.
    """

    def _parse(self):
        result = int.from_bytes(self.stream.read(64), byteorder="little", signed=False)
        return binaryToIntList(result)
