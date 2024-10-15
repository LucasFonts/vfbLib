from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr
from io import BytesIO
from struct import unpack
from typing import TYPE_CHECKING, Any
from vfbLib.parsers.value import read_doubles, read_value, read_floats

if TYPE_CHECKING:
    from io import BufferedReader
    from vfbLib.typing import ClassFlagDict


logger = logging.getLogger(__name__)

uint8 = 1
uint16 = 2
uint32 = 4


class StreamReader:
    encoding = "cp1252"
    stream: BufferedReader | BytesIO = BytesIO()

    def read_double(self):
        return read_doubles(1, self.stream)[0]

    def read_doubles(self, num):
        return read_doubles(num, self.stream)

    def read_float(self):
        return read_floats(1, self.stream)[0]

    def read_floats(self, num):
        return read_floats(num, self.stream)

    def read_int16(self) -> int:
        return int.from_bytes(self.stream.read(uint16), byteorder="little", signed=True)

    def read_int32(self) -> int:
        return int.from_bytes(self.stream.read(uint32), byteorder="little", signed=True)

    def read_str(self, size: int) -> str:
        return self.stream.read(size).decode(self.encoding)

    def read_uint8(self) -> int:
        return int.from_bytes(self.stream.read(uint8), byteorder="little", signed=False)

    def read_uint16(self) -> int:
        return int.from_bytes(
            self.stream.read(uint16), byteorder="little", signed=False
        )

    def read_uint32(self) -> int:
        return int.from_bytes(
            self.stream.read(uint32), byteorder="little", signed=False
        )

    def read_value(self, signed: bool = True):
        return read_value(self.stream, signed=signed)


class BaseParser(StreamReader):
    """
    Base class to parse data from a vfb file
    """

    master_count: int | None = None
    stream: BytesIO = BytesIO()
    ttStemsV_count: int | None = None
    ttStemsH_count: int | None = None

    def parse(
        self,
        stream: BytesIO,
        size: int,
        master_count: int | None = None,
        ttStemsV_count: int | None = None,
        ttStemsH_count: int | None = None,
    ):
        self.stream = BytesIO(stream.read(size))
        self.master_count = master_count
        self.ttStemsV_count = ttStemsV_count
        self.ttStemsH_count = ttStemsH_count

        decompiled = self._parse()

        # Make sure the parser consumed all of the data
        assert self.stream.read() == b""

        return decompiled

    def _parse(self) -> Any:
        """
        Custom parsing method. By default, it returns a human-readable hex string of the
        data.

        Returns:
            Any: _description_
        """
        return hexStr(self.stream.read())


class EncodedKeyValuesParser(BaseParser):
    __end__ = 0x64

    def _parse(self) -> list[dict[int, int]]:
        values = []
        while True:
            key = self.read_uint8()
            if key == self.__end__:
                break

            val = self.read_value()
            values.append({key: val})

        return values


class EncodedKeyValuesParser1742(EncodedKeyValuesParser):
    __end__ = 0x00


class EncodedValueParser(BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded value (1 value).
    """

    def _parse(self) -> int:
        value = self.read_value()
        return value


class EncodedValueListParser(BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded values.
    """

    def _parse(self) -> list[int]:
        values = []
        while True:
            try:
                val = self.read_value()
                values.append(val)
            except EOFError:
                logger.debug("EOF")
                return values


class EncodedValueListWithCountParser(BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded values. The list of values is
    preceded by a count value that specifies how many values should be read.
    """

    def _parse(self) -> dict[str, list[int]]:
        count = self.read_value()
        values: dict[str, list[int]] = {"values": []}
        for _ in range(count):
            val = self.read_value()
            values["values"].append(val)
        return values


class GaspParser(BaseParser):
    """
    A parser that reads data as an array representing Gasp table values.
    """

    def _parse(self):
        data = self.stream.read()
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
    def _parse(self):
        gid = int.from_bytes(self.stream.read(2), byteorder="little")
        nam = self.stream.read().decode("cp1252")
        return gid, nam


class OpenTypeClassFlagsParser(BaseParser):
    def _parse(self) -> ClassFlagDict:
        class_flags: ClassFlagDict = {}
        num_classes = self.read_value()
        for _ in range(num_classes):
            n = self.read_value()
            name = self.read_str(n)
            flag1 = self.read_value()
            flag2 = self.read_value()
            class_flags[name] = (flag1, flag2)
        return class_flags
