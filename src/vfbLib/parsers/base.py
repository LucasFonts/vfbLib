from __future__ import annotations

import logging
from io import BytesIO
from struct import unpack
from typing import TYPE_CHECKING, Any

from vfbLib import mapping_modes
from vfbLib.helpers import (
    deHexStr,
    double_size,
    hexStr,
    int8_size,
    int16_size,
    int32_size,
)
from vfbLib.parsers.value import read_value

if TYPE_CHECKING:
    from io import BufferedReader

    from vfbLib.typing import KerningClassFlagDict, MetricsClassFlagDict


logger = logging.getLogger(__name__)


class StreamReader:
    """
    Base class that reads values from the input stream.

    This is the parent class for the general BaseParser, from which all other parsers
    inherit, but it may be subclassed directly if more flexibility is needed.
    """

    def __init__(self) -> None:
        self.encoding = "cp1252"
        self.stream: BufferedReader | BytesIO = BytesIO()

    def read_double(self) -> float:
        """
        Return a double-precision float from the stream.

        Returns:
            float: The float
        """
        return self.read_doubles(1)[0]

    def read_doubles(self, num) -> tuple[float, ...]:
        """
        Return a tuple of `num` double-precision floats from the stream.

        Args:
            num (int): The number of double-precision floats to read from the stream

        Returns:
            tuple[float]: The tuple of floats
        """
        return unpack(num * "d", self.stream.read(num * double_size))

    def read_int8(self) -> int:
        """
        Return a signed 8-bit integer from the stream.

        Returns:
            int: The integer
        """
        return int.from_bytes(
            self.stream.read(int8_size), byteorder="little", signed=True
        )

    def read_int16(self) -> int:
        """
        Return a signed 16-bit integer from the stream.

        Returns:
            int: The integer
        """
        return int.from_bytes(
            self.stream.read(int16_size), byteorder="little", signed=True
        )

    def read_int32(self) -> int:
        """
        Return a signed 32-bit integer from the stream.

        Returns:
            int: The integer
        """
        return int.from_bytes(
            self.stream.read(int32_size), byteorder="little", signed=True
        )

    def read_str(self, size: int) -> str:
        """
        Return a string of the specified `size` from the current stream with the current
        encoding.

        Args:
            size (int): The size in bytes to be converted to a string

        Returns:
            str: The string
        """
        if size == 0:
            return ""
        return self.stream.read(size).decode(self.encoding)

    def read_str_with_len(self) -> str:
        """
        Read the length of a string from the current stream, then the string itself, and
        return the string.

        Returns:
            str: The string
        """
        size = self.read_value(signed=False)
        return self.read_str(size)

    def read_str_all(self) -> str:
        """
        Return the remaining bytes of the current stream as a string with the current
        encoding.

        Returns:
            str: The string
        """
        return self.stream.read().decode(self.encoding)

    def read_uint8(self) -> int:
        """
        Return an unsigned 8-bit integer from the stream.

        Returns:
            int: The integer
        """
        return int.from_bytes(
            self.stream.read(int8_size), byteorder="little", signed=False
        )

    def read_uint16(self) -> int:
        """
        Return an unsigned 16-bit integer from the stream.

        Returns:
            int: The integer
        """
        return int.from_bytes(
            self.stream.read(int16_size), byteorder="little", signed=False
        )

    def read_uint32(self) -> int:
        """
        Return an unsigned 32-bit integer from the stream.

        Returns:
            int: The integer
        """
        return int.from_bytes(
            self.stream.read(int32_size), byteorder="little", signed=False
        )

    def read_value(self, signed: bool = True) -> int:
        """
        Return an encoded integer value from the stream.

        Args:
            signed (bool, optional): Whether the value is interpreted as a signed value.
            Defaults to True.

        Returns:
            int: The integer
        """
        return read_value(self.stream, signed=signed)


class BaseParser(StreamReader):
    """
    Base class to parse data from a vfb file
    """

    def __init__(self) -> None:
        self.encoding = "cp1252"
        self.master_count: int = 0
        self.stream: BytesIO = BytesIO()
        self.ttStemsV_count: int | None = None
        self.ttStemsH_count: int | None = None

    def parse(
        self,
        stream: BytesIO,
        size: int,
        master_count: int = 0,
        ttStemsV_count: int | None = None,
        ttStemsH_count: int | None = None,
    ) -> Any:
        """
        Prepare the parsing of the stream, then call the specialized parser and return
        the decompiled VFB entry structure.

        The specialized parsing is done by calling the `_parse` method, which must be
        implemented for all entry parser sublasses.

        Args:
            stream (BytesIO): The stream to read from.
            size (int): The number of bytes that will be read from the input stream and
                parsed.
            master_count (int, optional): The number of masters in the font. This is
                needed for some multiple-master-enabled VFB parsers. Defaults to 0.
            ttStemsV_count (int | None, optional): The number of TrueType hinting stems
                in the vertical hint direction, This is needed for some
                TrueType-hinting-related parsers. Defaults to None.
            ttStemsH_count (int | None, optional): The number of TrueType hinting stems
                in the horizontal hint direction, This is needed for some
                TrueType-hinting-related parsers. Defaults to None.

        Raises:
            AssertionError: If bytes remain in the stream after the parsing finished.

        Returns:
            Any: The parsed structure. The type depends on the specific entry that is
            being parsed.
        """
        self.stream = BytesIO(stream.read(size))  # type: ignore
        self.master_count = master_count
        self.ttStemsV_count = ttStemsV_count
        self.ttStemsH_count = ttStemsH_count

        decompiled = self._parse()

        # Make sure the parser consumed all of the data
        remainder = self.stream.read()
        if remainder != b"":
            logger.error(f"Parser {self.__class__.__name__} did not consume all bytes.")
            logger.error(f"Remainder: {remainder!r}")
            raise AssertionError

        return decompiled

    def parse_hex(self, hexstr: str, master_count: int = 0):
        """
        Parse the data given in hex string format, e.g. "8c 8d 89 8b". Used for testing.

        Args:
            hexstr (str): The data
        """
        data = deHexStr(hexstr)
        return self.parse(BytesIO(data), len(data), master_count)

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
        """
        Parse and return the entry as a list of key-value-dictionaries. Both keys and
        values in the dictionary are integers.

        Returns:
            list[dict[int, int]]: The list of key-value dictionaries.
        """
        values = []
        while True:
            key = self.read_uint8()
            if key == self.__end__:
                break

            val = self.read_value()
            values.append({key: val})

        return values


class MappingModeParser(BaseParser):
    __end__ = 0x00

    def _parse(self) -> dict[str, str | int]:
        value: dict[str, str | int] = {}
        while True:
            key = self.read_uint8()
            if key == self.__end__:
                break

            v = self.read_value()

            if key == 1:
                value["mapping_mode"] = mapping_modes.get(v, str(v))
            elif key == 2:
                value["2"] = v
            elif key == 3:
                value["3"] = v
            elif key == 4:
                # encoding id:
                #   in mapping_mode 0:
                #      -1: glyph index mode
                #       0: imported encoding
                #       n: encoding id
                #   in mapping_mode 1:
                #      index into unicode_ranges from uranges.dat
                #   in mapping mode 3:
                #      index into codepages sorted by group, then name (?)
                value["mapping_id"] = v
            else:
                raise KeyError

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

    def _parse(self) -> list[int]:
        count = self.read_value()
        values: list[int] = []  # TODO: We don't need the dict
        for _ in range(count):
            val = self.read_value()
            values.append(val)
        return values


class GlyphEncodingParser(BaseParser):
    def _parse(self):
        gid = self.read_uint16()
        nam = self.stream.read().decode("cp1252")
        return gid, nam


class OpenTypeKerningClassFlagsParser(BaseParser):
    def _parse(self) -> KerningClassFlagDict:
        class_flags: KerningClassFlagDict = {}
        num_classes = self.read_value()
        for _ in range(num_classes):
            name = self.read_str_with_len()
            flag1 = self.read_value()
            flag2 = self.read_value()
            class_flags[name] = (flag1, flag2)
        return class_flags


class OpenTypeMetricsClassFlagsParser(BaseParser):
    def _parse(self) -> MetricsClassFlagDict:
        class_flags: MetricsClassFlagDict = {}
        num_classes = self.read_value()
        for _ in range(num_classes):
            name = self.read_str_with_len()
            flag1 = self.read_value()
            flag2 = self.read_value()
            flag3 = self.read_value()
            class_flags[name] = (flag1, flag2, flag3)
        return class_flags
