from vfbLib.parsers import BaseParser
from struct import unpack


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
            values.append(unpack(cls.__fmt__, cls.stream.read(cls.__size__)))

        return values


class IntParser(BaseParser):
    """
    A parser that reads data as UInt16.
    """

    @classmethod
    def _parse(cls):
        return int.from_bytes(
            cls.stream.read(), byteorder="little", signed=False
        )


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
        return int.from_bytes(
            cls.stream.read(), byteorder="little", signed=True
        )
