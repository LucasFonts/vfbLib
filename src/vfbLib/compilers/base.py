from __future__ import annotations

from io import BytesIO
from struct import pack
from typing import TYPE_CHECKING

from vfbLib.compilers.value import write_value, write_value_long
from vfbLib.helpers import deHexStr, hexStr, int8_size, int16_size, int32_size

if TYPE_CHECKING:
    from io import BufferedWriter
    from typing import Any, Iterable

    from vfbLib.typing import KerningClassFlagDict, MetricsClassFlagDict


# Compilers for VFB entries


class StreamWriter:
    """
    Base compiler class that writes values to the output stream.
    This is the parent class for the general BaseCompiler, from which all other
    compilers inherit, but it may be subclassed directly if more flexibility is needed.
    """

    def __init__(self) -> None:
        self.encoding = "cp1252"
        self.stream: BufferedWriter | BytesIO = BytesIO()

    def write_bytes(self, value: bytes) -> None:
        """
        Write binary data to the stream.

        Args:
            value (bytes): The data.
        """
        self.stream.write(value)

    def write_double(self, value: float) -> None:
        """
        Write a double-precision float value to the stream.

        Args:
            value (float): The float value to write.
        """
        self.stream.write(pack("d", value))

    def write_doubles(self, values: Iterable[float]) -> None:
        """
        Write several double-precision floats to the stream.

        Args:
            values (Iterable[float]): The sequence of double-precision floats to write.
        """
        for f in values:
            self.write_double(f)

    def write_int16(self, value: int) -> None:
        """
        Write a signed 16-bit integer to the stream.

        Args:
            value (int): The integer value to write.
        """
        self.stream.write(value.to_bytes(int16_size, byteorder="little", signed=True))

    def write_int32(self, value: int) -> None:
        """
        Write a signed 32-bit integer to the stream.

        Args:
            value (int): The integer value to write.
        """
        self.stream.write(value.to_bytes(int32_size, byteorder="little", signed=True))

    def write_str(self, value: str | None, pad: int = 0) -> None:
        """
        Write a string to the stream. The string is encoded with
        `StreamWriter.encoding`.

        Args:
            value (str | None): The string to write.
            pad (int, optional): Pad the string to the given length with null bytes.
                Defaults to 0.
        """
        if value is None:
            value = ""
        enc = value.encode(self.encoding)
        if len(enc) < pad:
            enc += b"\00" * (pad - len(enc))
        self.stream.write(enc)

    def write_str_with_len(self, value: str | None) -> None:
        """
        Write the length of a string to the stream, then the string itself. The string
        is encoded with `StreamWriter.encoding`.

        Args:
            value (str | None): The string to write.
        """
        if value is None:
            value = ""
        enc = value.encode(self.encoding)
        self.write_value(len(enc))
        self.stream.write(enc)

    def write_uint8(self, value: int) -> None:
        """
        Write a uint8 value to the stream.

        Args:
            value (int): The integer to write.
        """
        self.stream.write(value.to_bytes(int8_size, byteorder="little", signed=False))

    def write_uint16(self, value: int) -> None:
        """
        Write a uint16 value to the stream.

        Args:
            value (int): The integer to write.
        """
        self.stream.write(value.to_bytes(int16_size, byteorder="little", signed=False))

    def write_uint32(self, value: int) -> None:
        """
        Write an unsigned 32-bit integer to the stream.

        Args:
            value (int): The integer value to write.
        """
        self.stream.write(value.to_bytes(int32_size, byteorder="little", signed=False))

    def write_value(self, value: int, shortest=True, signed: bool = True) -> None:
        """
        Encode and write an int value to the stream. Optionally don't apply the length
        encoding optimization.

        Args:
            value (int): The value to write to the stream.
            shortest (bool, optional): Whether to write the shortest possible
                representation. Defaults to True.
        """
        if shortest:
            write_value(value, self.stream, signed)
        else:
            write_value_long(value, self.stream, signed)


class BaseCompiler(StreamWriter):
    """
    Base class to compile vfb data.
    """

    def compile(self, data: Any, master_count: int = 0) -> bytes:
        """
        Compile the JSON-like main data structure and return the compiled binary data.

        The actual compilation is done by calling the `_compile` method, which must be
        implemented for all specialized compiler subclasses.

        Args:
            data (Any): The main data structure.
            master_count (int, optional): The number of masters. Defaults to 0.

        Returns:
            bytes: The compiled binary data.
        """
        self.master_count = master_count
        self.stream = BytesIO()
        self._compile(data)
        return self.stream.getvalue()

    def compile_hex(self, data: Any, master_count: int = 0) -> str:
        """
        Compile the data given into a hex string format, e.g. "8c 8d 89 8b". Used for
        testing.

        Args:
            data (Any): The input data
            master_count (int, optional): Number of masters. Defaults to 0.

        Returns:
            str: The hex string
        """
        b = self.compile(data, master_count)
        return hexStr(b)

    def _compile(self, data: Any) -> None:
        raise NotImplementedError

    @classmethod
    def merge(cls, masters_data: list[Any], data: Any) -> None:
        """
        Merge the data of additional masters into the main data structure. This operates
        on the uncompiled JSON-like data structure.

        Args:
            masters_data (list[Any]): The additional masters data as a list with one
                entry per master.
            data (Any): The main data structure.
        """
        # Must be implemented for compilers that need it, e.g. the GlyphCompiler.
        pass


class EncodedValueListCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        for value in data:
            self.write_value(value)


class EncodedValueListWithCountCompiler(BaseCompiler):
    def _compile(self, data: list[int]) -> None:
        self.write_value(len(data))
        for value in data:
            self.write_value(value)


class GlyphEncodingCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        """
        Compile the data into the format used by a glyph encoding entry.

        Args:
            data (tuple[int, str]): A tuple containing the glyph ID and the glyph name.
        """
        gid, name = data
        self.write_uint16(gid)
        self.write_str(name)  # XXX: Does it have to be cp1252?


class HexStringCompiler(BaseCompiler):
    def _compile(self, data: str | None) -> None:
        """
        Compile the data given in hex string format to the stream as bytes.

        This can be used as a fallback for unsupported entries as long as the hex data
        is known, e.g. for end markers or constants.

        Args:
            data (str | None): The hex string data, e.g. "203955", or None.
        """
        if not data:
            return

        self.write_bytes(deHexStr(data))


mapping_modes = {
    0: "names_or_index",
    1: "unicode_ranges",
    3: "codepages",
}


class MappingModeCompiler(BaseCompiler):
    def _compile(self, data: dict[str, str | int]) -> None:
        rev_map = {v: k for k, v in mapping_modes.items()}
        self.write_uint8(1)
        self.write_value(rev_map[data["mapping_mode"]])
        self.write_uint8(2)
        self.write_value(data["2"])
        self.write_uint8(3)
        self.write_value(data["3"])
        self.write_uint8(4)
        self.write_value(data["mapping_id"])
        self.write_uint8(0)


class OpenTypeKerningClassFlagsCompiler(BaseCompiler):
    def _compile(self, data: KerningClassFlagDict) -> None:
        self.write_value(len(data), signed=False)
        for name, flags in data.items():
            self.write_str_with_len(name)
            flag1, flag2 = flags
            self.write_value(flag1, signed=False)
            self.write_value(flag2, signed=False)


class OpenTypeMetricsClassFlagsCompiler(BaseCompiler):
    def _compile(self, data: MetricsClassFlagDict) -> None:
        self.write_value(len(data), signed=False)
        for name, flags in data.items():
            self.write_str_with_len(name)
            flag1, flag2, flag3 = flags
            self.write_value(flag1, signed=False)
            self.write_value(flag2, signed=False)
            self.write_value(flag3, signed=False)
