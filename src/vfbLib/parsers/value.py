from __future__ import annotations

from typing import TYPE_CHECKING

from vfbLib.helpers import int8_size, int32_size

if TYPE_CHECKING:
    from io import BufferedReader, BytesIO


def read_value(stream: BufferedReader | BytesIO, signed=True) -> int:
    """
    Read an encoded value from the stream, decode it to integer and return it.

    The storage format in the stream of the "encoded value" is the same as described in
    the Type 1 specification, p. 48, "Charstring Number Encoding"
    <https://adobe-type-tools.github.io/font-tech-notes/pdfs/T1_SPEC.pdf>.

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
        int: The decoded value.
    """
    val = int.from_bytes(stream.read(int8_size), byteorder="little")
    if val == 0:
        raise EOFError

    if val < 0x20:
        raise ValueError

    elif val < 0xF7:
        # -107 to 107, represented by 1 byte
        return val - 0x8B

    elif val <= 0xFA:
        # 108 to 1131, represented by 2 bytes
        val2 = int.from_bytes(stream.read(int8_size), byteorder="little")
        # val - 0x8B + (val - 0xF7) * 0xFF + val2
        return 0x100 * val - 0xF694 + val2

    elif val <= 0xFE:
        # -108 to -1131, represented by 2 bytes
        val2 = int.from_bytes(stream.read(int8_size), byteorder="little")
        # 0x8F - val - (val - 0xFB) * 0xFF - val2
        return -0x100 * val + 0xFA94 - val2

    elif val == 0xFF:
        # 32 bit integer follows
        # FIXME: The Type1 spec says that it is always a signed int.
        decoded = int.from_bytes(
            stream.read(int32_size), byteorder="big", signed=signed
        )
        return decoded

    raise ValueError
