from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr
from io import BufferedReader, BytesIO
from struct import unpack
from typing import TYPE_CHECKING, Any
from vfbLib.parsers.value import read_doubles, read_encoded_value, read_floats

if TYPE_CHECKING:
    from vfbLib.typing import ClassFlagDict


logger = logging.getLogger(__name__)

uint8 = 1
uint16 = 2
uint32 = 4


class BaseParser:
    """
    Base class to parse data from a vfb file
    """

    encoding = "cp1252"
    expected_decompiled_type = str
    master_count: int | None = None
    stream: BytesIO = BytesIO()
    ttStemsV_count: int | None = None
    ttStemsH_count: int | None = None

    def parse(
        self,
        stream: BufferedReader,
        size: int,
        master_count: int | None = None,
        ttStemsV_count: int | None = None,
        ttStemsH_count: int | None = None,
    ):
        self.stream = BytesIO(stream.read(size))
        self.master_count = master_count
        self.ttStemsV_count = ttStemsV_count
        self.ttStemsH_count = ttStemsH_count
        return self._parse()
        # decompiled = self._parse()
        # if not isinstance(decompiled, self.expected_decompiled_type):
        #     logger.error(
        #         f"Expected '{__class__.__name__}' to return an instance of "
        #         f"{self.expected_decompiled_type.__name__}, got "
        #         f"{type(decompiled).__name__} instead."
        #     )
        #     raise TypeError

        # return decompiled

    def _parse(self) -> Any:
        return hexStr(self.stream.read())

    def read_double(self, stream=None):
        if stream is None:
            stream = self.stream
        return read_doubles(1, stream)[0]

    def read_doubles(self, num, stream=None):
        if stream is None:
            stream = self.stream
        return read_doubles(num, stream)

    def read_float(self, stream=None):
        if stream is None:
            stream = self.stream
        return read_floats(1, stream)[0]

    def read_floats(self, num, stream=None):
        if stream is None:
            stream = self.stream
        return read_floats(num, stream)

    def read_int16(self, stream=None) -> int:
        if stream is None:
            stream = self.stream
        return int.from_bytes(stream.read(uint16), byteorder="little", signed=True)

    def read_int32(self, stream=None) -> int:
        if stream is None:
            stream = self.stream
        return int.from_bytes(stream.read(uint32), byteorder="little", signed=True)

    def read_uint8(self, stream=None) -> int:
        if stream is None:
            stream = self.stream
        return int.from_bytes(stream.read(uint8), byteorder="little", signed=False)

    def read_uint16(self, stream=None) -> int:
        if stream is None:
            stream = self.stream
        return int.from_bytes(stream.read(uint16), byteorder="little", signed=False)

    def read_uint32(self, stream=None) -> int:
        if stream is None:
            stream = self.stream
        return int.from_bytes(stream.read(uint32), byteorder="little", signed=False)


class ReturnsDict:
    expected_decompiled_type = dict


class ReturnsFloat:
    expected_decompiled_type = float


class ReturnsInt:
    expected_decompiled_type = int


class ReturnsList:
    expected_decompiled_type = list


class ReturnsTuple:
    expected_decompiled_type = tuple


class EncodedKeyValuesParser(ReturnsList, BaseParser):
    __end__ = 0x64

    def _parse(self) -> list[dict[int, int]]:
        values = []
        while True:
            key = self.read_uint8()
            if key == self.__end__:
                break

            val = read_encoded_value(self.stream)
            values.append({key: val})

        return values


class EncodedKeyValuesParser1742(EncodedKeyValuesParser):
    __end__ = 0x00


class EncodedValueParser(ReturnsInt, BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded value (1 value).
    """

    def _parse(self) -> int:
        value = read_encoded_value(self.stream)
        assert self.stream.read() == b""
        return value


class EncodedValueListParser(ReturnsList, BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded values.
    """

    def _parse(self) -> list[int]:
        values = []
        while True:
            try:
                val = read_encoded_value(self.stream)
                values.append(val)
            except EOFError:
                logger.debug("EOF")
                return values


class EncodedValueListWithCountParser(ReturnsDict, BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded values. The list of values is
    preceded by a count value that specifies how many values should be read.
    """

    def _parse(self) -> dict[str, list[int]]:
        count = read_encoded_value(self.stream)
        values: dict[str, list[int]] = {"values": []}
        for _ in range(count):
            val = read_encoded_value(self.stream)
            values["values"].append(val)
        return values


class GaspParser(ReturnsList, BaseParser):
    """
    A parser that reads data as an array representing Gasp table values.
    """

    def _parse(self):
        data = self.stream.read()
        # self.stream.getbuffer().nbytes
        gasp = unpack(f"<{len(data) // 2}H", data)
        it = iter(gasp)
        return [
            {
                "maxPpem": a,
                "flags": b,
            }
            for a, b in zip(it, it)
        ]


class GlyphEncodingParser(ReturnsTuple, BaseParser):
    def _parse(self):
        gid = int.from_bytes(self.stream.read(2), byteorder="little")
        nam = self.stream.read().decode("cp1252")
        return gid, nam


class OpenTypeClassFlagsParser(ReturnsDict, BaseParser):
    def _parse(self) -> ClassFlagDict:
        class_flags: ClassFlagDict = {}
        num_classes = read_encoded_value(self.stream)
        for _ in range(num_classes):
            n = read_encoded_value(self.stream)
            name = self.stream.read(n).decode(self.encoding)
            flag1 = read_encoded_value(self.stream)
            flag2 = read_encoded_value(self.stream)
            class_flags[name] = (flag1, flag2)
        return class_flags
