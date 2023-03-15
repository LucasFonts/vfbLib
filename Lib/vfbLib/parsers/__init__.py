from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr
from io import BufferedReader, BytesIO
from struct import unpack
from typing import TYPE_CHECKING, Any, Dict, List
from vfbLib.parsers.value import read_doubles, read_encoded_value, read_floats

if TYPE_CHECKING:
    from vfbLib.typing import ClassFlagDict


logger = logging.getLogger(__name__)

uint8 = 1
uint16 = 2
uint32 = 4


class BaseParser:
    """
    Base class to read data from a vfb file
    """

    master_count: int | None = None
    stream: BytesIO = BytesIO()

    @classmethod
    def parse(
        cls,
        stream: BufferedReader,
        size: int,
        master_count: int | None = None,
    ):
        cls.stream = BytesIO(stream.read(size))
        cls.master_count = master_count
        return cls._parse()

    @classmethod
    def _parse(cls) -> Any:
        return hexStr(cls.stream.read())

    @classmethod
    def read_double(cls, stream=None):
        if stream is None:
            stream = cls.stream
        return read_doubles(1, stream)[0]
    
    @classmethod
    def read_doubles(cls, num, stream=None):
        if stream is None:
            stream = cls.stream
        return read_doubles(num, stream)

    @classmethod
    def read_float(cls, stream=None):
        if stream is None:
            stream = cls.stream
        return read_floats(1, stream)[0]
    
    @classmethod
    def read_floats(cls, num, stream=None):
        if stream is None:
            stream = cls.stream
        return read_floats(num, stream)

    @classmethod
    def read_int16(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(stream.read(uint16), byteorder="little", signed=True)

    @classmethod
    def read_int32(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(stream.read(uint32), byteorder="little", signed=True)

    @classmethod
    def read_uint8(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(stream.read(uint8), byteorder="little", signed=False)

    @classmethod
    def read_uint16(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(stream.read(uint16), byteorder="little", signed=False)

    @classmethod
    def read_uint32(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(stream.read(uint32), byteorder="little", signed=False)


class EncodedKeyValuesParser(BaseParser):
    __end__ = 0x64

    @classmethod
    def _parse(cls) -> List[Dict[int, int]]:
        values = []
        while True:
            key = cls.read_uint8()
            if key == cls.__end__:
                break

            val = read_encoded_value(cls.stream)
            values.append({key: val})

        return values


class EncodedKeyValuesParser1742(EncodedKeyValuesParser):
    __end__ = 0x00


class EncodedValueParser(BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded value (1 value).
    """

    @classmethod
    def _parse(cls) -> int:
        value = read_encoded_value(cls.stream)
        assert cls.stream.read() == b""
        return value


class EncodedValueListParser(BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded values.
    """

    @classmethod
    def _parse(cls) -> List[int]:
        values = []
        while True:
            try:
                val = read_encoded_value(cls.stream)
                values.append(val)
            except EOFError:
                logger.debug("EOF")
                return values


class EncodedValueListWithCountParser(BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded values. The list of values is
    preceded by a count value that specifies how many values should be read.
    """

    @classmethod
    def _parse(cls) -> Dict[str, List[int]]:
        count = read_encoded_value(cls.stream)
        values: Dict[str, List[int]] = {"values": []}
        for _ in range(count):
            val = read_encoded_value(cls.stream)
            values["values"].append(val)
        return values


class GaspParser(BaseParser):
    """
    A parser that reads data as an array representing Gasp table values.
    """

    @classmethod
    def _parse(cls):
        data = cls.stream.read()
        # cls.stream.getbuffer().nbytes
        gasp = unpack(f"<{len(data) // 2}H", data)
        it = iter(gasp)
        return [
            {
                "maxPpem": a,
                "flags": b,
            }
            for a, b in zip(it, it)
        ]


class GlyphEncodingParser(BaseParser):
    @classmethod
    def _parse(cls):
        return 0  # FIXME: Encoding is ignored for now
        gid = int.from_bytes(cls.stream.read(2), byteorder="little")
        nam = cls.stream.read().decode("ascii")
        return gid, nam


class OpenTypeClassFlagsParser(BaseParser):
    @classmethod
    def _parse(cls) -> ClassFlagDict:
        class_flags: ClassFlagDict = {}
        num_classes = read_encoded_value(cls.stream)
        for _ in range(num_classes):
            n = read_encoded_value(cls.stream)
            name = cls.stream.read(n).decode("cp1252")
            flag1 = read_encoded_value(cls.stream)
            flag2 = read_encoded_value(cls.stream)
            class_flags[name] = (flag1, flag2)
        return class_flags
