from __future__ import annotations

from io import BytesIO
from struct import pack
from typing import TYPE_CHECKING, Any

from fontTools.misc.textTools import hexStr

from vfbLib.compilers.value import write_value, write_value_long
from vfbLib.helpers import uint8, uint16  # , uint32

if TYPE_CHECKING:
    from io import BufferedWriter


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
        raise NotImplementedError

    def write_doubles(self, values: list[float]) -> None:
        """Write several doubles to the stream.

        Args:
            values (list[float]): _description_
        """
        raise NotImplementedError

    def write_float(self, value: float, fmt: str = "d") -> None:
        """
        Write a float value to the stream.
        """
        encoded = pack(fmt, value)
        self.stream.write(encoded)

    def write_floats(self, values: list[float]) -> None:
        raise NotImplementedError

    def write_int16(self, value: int) -> None:
        raise NotImplementedError

    def write_int32(self, value: int) -> None:
        raise NotImplementedError

    def write_str(self, value: str, pad: int = 0) -> None:
        # XXX: Pad with 0 bytes to given length
        self.stream.write(value.encode(self.encoding))

    def write_uint8(self, value: int) -> None:
        """
        Write a uint8 value to the stream.
        """
        self.stream.write(value.to_bytes(uint8, byteorder="little", signed=False))

    def write_uint16(self, value: int) -> None:
        self.stream.write(value.to_bytes(uint16, byteorder="little", signed=False))

    def write_uint32(self, value: int) -> None:
        raise NotImplementedError

    def write_value(self, value: int, shortest=True) -> None:
        """
        Encode and write an int value to the stream. Optionally don't apply the length
        encoding optimization.

        Args:
            value (int): The value to write to the stream.
            shortest (bool, optional): Whether to write the shortest possible
                representation. Defaults to True.
        """
        if shortest:
            write_value(value, self.stream)
        else:
            write_value_long(value, self.stream)


class BaseCompiler(StreamWriter):
    """
    Base class to compile vfb data.
    """

    def compile(self, data: Any, master_count: int = 0) -> bytes:
        """
        Compile the JSON-like main data structure and return the compiled binary data.

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
            masters_data (List[Any]): The additional masters data as a list with one
                entry per master.
            data (Any): The main data structure.
        """
        # Must be implemented for compilers that need it, e.g. the GlyphCompiler.
        pass


class GlyphEncodingCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        gid, name = data
        self.write_uint16(gid)
        self.write_str(name)  # XXX: Does it have to be cp1252?
