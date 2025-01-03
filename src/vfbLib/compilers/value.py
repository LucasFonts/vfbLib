from __future__ import annotations

from struct import pack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import BufferedWriter, BytesIO


def write_value(value: int, stream: BufferedWriter | BytesIO, signed=True) -> None:
    """
    Encode and write an int value to the stream in the shortest possible representation.

    Args:
        value (int): The value to write to the stream.
        stream (BufferedWriter | BytesIO): The output stream.
        signed (bool, optional): Whether the value is signed. Defaults to True.
    """
    if -107 <= value <= 107:
        # 1-byte representation
        encoded = pack(">B", (value + 0x8B))
    elif 107 < value <= 1131:
        # 2-byte representation
        encoded = pack(">H", (value + 0xF694))
    elif -1131 <= value < -107:
        # 2-byte representation, negative values
        encoded = pack(">H", (-value + 0xFA94))
    else:
        # 5-byte representation
        write_value_long(value, stream, signed)
        return

    stream.write(encoded)


def write_value_long(value: int, stream: BufferedWriter | BytesIO, signed=True) -> None:
    """
    Write an integer value to the stream using the longest encoding (4 bytes plus
    marker byte).

    Args:
        value (int): The value to write to the stream.
        stream (BufferedWriter | BytesIO): The output stream.
        signed (bool, optional): Whether the value is signed. Defaults to True.
    """
    fmt = "i" if signed else "I"
    encoded = pack(f">B{fmt}", 0xFF, value)
    stream.write(encoded)
