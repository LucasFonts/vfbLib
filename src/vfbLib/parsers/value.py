from __future__ import annotations

from struct import unpack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import BufferedReader, BytesIO


def read_value(stream: BufferedReader | BytesIO, signed=True) -> int:
    """
    Read an encoded value from the stream, decode it to integer and return it.

    Args:
        stream (BufferedReader | BytesIO): The input stream.
        signed (bool, optional): Whether to interpret the value as a signed integer.
            Defaults to True.

    Raises:
        EOFError: When a 0 byte is encountered while reading the stream.
        ValueError: When the byte that was read from the stream is < 0x20.
        ValueError: When the byte that was read from the stream has any other undefined
            value.

    Returns:
        int: _description_
    """
    val = int.from_bytes(stream.read(1), byteorder="little")
    if val == 0:
        raise EOFError

    if val < 0x20:
        raise ValueError

    elif val < 0xF7:
        # -107 to 107, represented by 1 byte
        return val - 0x8B

    elif val <= 0xFA:
        # 108 to 1131, represented by 2 bytes
        val2 = int.from_bytes(stream.read(1), byteorder="little")
        # val - 0x8B + (val - 0xF7) * 0xFF + val2
        return 0x100 * val - 0xF694 + val2

    elif val <= 0xFE:
        # -108 to -1131, represented by 2 bytes
        val2 = int.from_bytes(stream.read(1), byteorder="little")
        # 0x8F - val - (val - 0xFB) * 0xFF - val2
        return -0x100 * val + 0xFA94 - val2

    elif val == 0xFF:
        # 4-byte integer follows
        decoded = int.from_bytes(stream.read(4), byteorder="big", signed=signed)
        return decoded

    raise ValueError


def read_doubles(num: int, stream: BufferedReader | BytesIO) -> tuple[float]:
    """
    Read a number `num` of double-precision floats from the stream and return them.

    Args:
        num (int): The number of values to be read.
        stream (BufferedReader | BytesIO): The input stream.

    Returns:
        tuple[float]: The tuple of double-precision floats.
    """
    return unpack(num * "d", stream.read(num * 8))


def read_floats(num: int, stream: BufferedReader | BytesIO) -> tuple[float]:
    """
    Read a number `num` of floats from the stream and return them.

    Args:
        num (int): The number of values to be read.
        stream (BufferedReader | BytesIO): The input stream.

    Returns:
        tuple[float]: The tuple of floats.
    """
    return unpack(num * "f", stream.read(num * 4))
