from __future__ import annotations

import logging

from vfbLib.parsers import BaseParser
from struct import unpack


logger = logging.getLogger(__name__)


class DoubleParser(BaseParser):
    """
    A parser that reads data as a double-size float.
    """

    @classmethod
    def _parse(cls):
        return unpack("d", cls.stream.read(8))[0]


class FloatListParser(BaseParser):
    """
    A parser that reads data as a list of floats.
    """

    __size__ = 4
    __fmt__ = "f"

    @classmethod
    def _parse(cls):
        values = []
        for _ in range(cls.stream.getbuffer().nbytes // cls.__size__):
            values.extend(unpack(cls.__fmt__, cls.stream.read(cls.__size__)))

        return values


class DoubleListParser(FloatListParser):
    """
    A parser that reads data as a list of doubles.
    """

    __size__ = 8
    __fmt__ = "d"


class IntParser(BaseParser):
    """
    A parser that reads data as UInt16.
    """

    @classmethod
    def _parse(cls):
        return int.from_bytes(cls.stream.read(), byteorder="little", signed=False)


class IntListParser(BaseParser):
    """
    A parser that reads data as a list of UInt16.
    """

    __size__ = 4

    @classmethod
    def _parse(cls):
        values = []
        for _ in range(cls.stream.getbuffer().nbytes // cls.__size__):
            values.append(
                int.from_bytes(
                    cls.stream.read(cls.__size__),
                    byteorder="little",
                    signed=False,
                )
            )
        return values


class PanoseParser(BaseParser):
    """
    A parser that reads data as an array representing PANOSE values.
    """

    @classmethod
    def _parse(cls):
        return unpack("<10b", cls.stream.read())


class SignedIntParser(BaseParser):
    """
    A parser that reads data as signed Int16.
    """

    @classmethod
    def _parse(cls):
        return int.from_bytes(cls.stream.read(), byteorder="little", signed=True)
