from __future__ import annotations

from fontTools.misc.textTools import hexStr
from io import BufferedReader, BytesIO
from struct import unpack
from typing import Any, Dict, List, Tuple


uint8 = 1
uint16 = 2
uint32 = 4


def read_encoded_value(
    stream: BufferedReader | BytesIO, debug=False, signed=True
) -> int:
    val = int.from_bytes(stream.read(1), byteorder="little")
    if val == 0:
        raise EOFError

    if debug:
        print("Read:", hex(val))

    if val < 0x20:
        if debug:
            print(f"  Illegal value {hex(val)}. Rest of stream:")
            print(hexStr(stream.read()))
        raise ValueError

    elif val < 0xF7:
        decoded = val - 0x8B
        if debug:
            print(f"  {hex(val)} - 0x8b = {val - 0x8b}")
        return decoded

    elif val <= 0xFA:
        val2 = int.from_bytes(stream.read(1), byteorder="little")
        if debug:
            print(f"  Read next: {hex(val2)}")
        decoded = val - 0x8B + (val - 0xF7) * 0xFF + val2
        if debug:
            print(
                f"    {hex(val)} - 0x8b + {val - 0xf7} * 0xff + {hex(val2)} = {decoded}"
            )
        return decoded

    elif val <= 0xFE:
        # Negative
        # FIXME

        val2 = int.from_bytes(stream.read(1), byteorder="little")
        # fb 1f -> 0x8f - 0xfb - 0x1f
        decoded = 0x8F - val - (val - 0xFB) * 0xFF - val2
        if debug:
            print(
                f"    0x8f - {hex(val)} - {val - 0xf7} * 0xff - {hex(val2)} = {decoded}"
            )
        return decoded

    elif val == 0xFF:
        # 4-byte integer follows
        decoded = int.from_bytes(
            stream.read(4), byteorder="big", signed=signed
        )
        if debug:
            print(f"  Read next 4 bytes: {decoded}")
        return decoded

    raise ValueError


def read_double(num, stream):
    return unpack(num * "d", stream.read(num * 8))


def read_float(num, stream):
    return unpack(num * "f", stream.read(num * 4))


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
    def read_double(cls, num, stream=None):
        if stream is None:
            stream = cls.stream
        return read_double(num, stream)

    @classmethod
    def read_float(cls, num, stream=None):
        if stream is None:
            stream = cls.stream
        return read_float(num, stream)

    @classmethod
    def read_int16(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(
            stream.read(uint16), byteorder="little", signed=True
        )

    @classmethod
    def read_int32(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(
            stream.read(uint32), byteorder="little", signed=True
        )

    @classmethod
    def read_uint8(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(
            stream.read(uint8), byteorder="little", signed=False
        )

    @classmethod
    def read_uint16(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(
            stream.read(uint16), byteorder="little", signed=False
        )

    @classmethod
    def read_uint32(cls, stream=None) -> int:
        if stream is None:
            stream = cls.stream
        return int.from_bytes(
            stream.read(uint32), byteorder="little", signed=False
        )


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
                # print("EOF")
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
    def _parse(cls) -> Dict[str, Tuple[int, int]]:
        class_flags: Dict[str, Tuple[int, int]] = {}
        num_classes = read_encoded_value(cls.stream)
        for _ in range(num_classes):
            n = read_encoded_value(cls.stream)
            name = cls.stream.read(n).decode("cp1252")
            flag1 = read_encoded_value(cls.stream)
            flag2 = read_encoded_value(cls.stream)
            class_flags[name] = (flag1, flag2)
        return class_flags


class StringParser(BaseParser):
    """
    A parser that reads data as ASCII-encoded strings.
    """

    @classmethod
    def _parse(cls):
        return cls.stream.read().decode("cp1252").strip("\u0000")
