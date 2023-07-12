from __future__ import annotations

from io import BytesIO
from struct import pack
from typing import Any
from vfbLib.compilers.value import write_encoded_value, write_value_5


# Compilers for VFB entries


class BaseCompiler:
    """
    Base class to compile vfb data
    """

    @classmethod
    def compile(cls, data: Any) -> bytes:
        cls.stream = BytesIO()
        cls._compile(data)
        return cls.stream.getvalue()

    @classmethod
    def _compile(cls, data: Any) -> None:
        raise NotImplementedError

    @classmethod
    def write_bytes(cls, value: bytes) -> None:
        """
        Write a bytes value to the stream
        """
        cls.stream.write(value)

    @classmethod
    def write_encoded_value(cls, value: int, shortest=True) -> None:
        """
        Encode and write an int value to the stream. Optionally don't apply the length
        encoding optimization.
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
        Write a 1-byte unsigned value to the stream
        """
        encoded = pack(">B", value)
        cls.stream.write(encoded)

    @classmethod
    def write_uint8(cls, value: int) -> None:
        """
        Write a uint8 value to the stream
        """
        encoded = pack(">H", value)
        cls.stream.write(encoded)
