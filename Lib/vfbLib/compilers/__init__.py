from __future__ import annotations

from io import BytesIO
from struct import pack
from typing import Any
from vfbLib.compilers.value import write_encoded_value, write_value_5


# Compilers for VFB entries


class BaseCompiler:
    """
    Base class to compile vfb data.
    """

    @classmethod
    def compile(cls, data: Any, master_count: int = 0) -> bytes:
        """
        Compile the JSON-like main data structure and return the compiled binary data.

        Args:
            data (Any): The main data structure.
            master_count (int, optional): The number of masters. Defaults to 0.

        Returns:
            bytes: The compiled binary data.
        """
        cls.master_count = master_count
        cls.stream = BytesIO()
        cls._compile(data)
        return cls.stream.getvalue()

    @classmethod
    def _compile(cls, data: Any) -> None:
        raise NotImplementedError

    @classmethod
    def merge(cls, masters_data: Any, data: Any, master_count: int = 0) -> Any:
        """
        Merge the data of additional masters into the main data structure. This operates
        on the uncompiled JSON-like data structure.

        Args:
            masters_data (Any): The additional masters data.
            data (Any): The main data structure.
            master_count (int, optional): The number of masters. Defaults to 0.

        Returns:
            Any: The merged main data structure.
        """
        # Must be implemented for compilers that need it, e.g. the GlyphCompiler.
        pass

    @classmethod
    def write_bytes(cls, value: bytes) -> None:
        """
        Write binary data to the stream.

        Args:
            value (bytes): The data.
        """
        cls.stream.write(value)

    @classmethod
    def write_encoded_value(cls, value: int, shortest=True) -> None:
        """
        Encode and write an int value to the stream. Optionally don't apply the length
        encoding optimization.

        Args:
            value (int): The value to write to the stream.
            shortest (bool, optional): Whether to write in the shortest possible
                notation. Defaults to True.
        """
        if shortest:
            write_encoded_value(value, cls.stream)
        else:
            write_value_5(value, cls.stream)

    @classmethod
    def write_float(cls, value: float, fmt: str = "d") -> None:
        """
        Write a float value to the stream.
        """
        encoded = pack(fmt, value)
        cls.stream.write(encoded)

    @classmethod
    def write_uint1(cls, value: int) -> None:
        """
        Write a 1-byte unsigned value to the stream.
        """
        encoded = pack(">B", value)
        cls.stream.write(encoded)

    @classmethod
    def write_uint8(cls, value: int) -> None:
        """
        Write a uint8 value to the stream.
        """
        encoded = pack(">H", value)
        cls.stream.write(encoded)
