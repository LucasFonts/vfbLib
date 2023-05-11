from __future__ import annotations

from io import BufferedReader, BytesIO
from struct import unpack


def read_encoded_value(stream: BufferedReader | BytesIO, signed=True) -> int:
    val = int.from_bytes(stream.read(1), byteorder="little")
    if val == 0:
        raise EOFError

    if val < 0x20:
        raise ValueError

    elif val < 0xF7:
        # -107 to 107, represented by 1 byte
        decoded = val - 0x8B
        return decoded

    elif val <= 0xFA:
        # 108 to 1131, represented by 2 bytes
        val2 = int.from_bytes(stream.read(1), byteorder="little")
        decoded = val - 0x8B + (val - 0xF7) * 0xFF + val2
        return decoded

    elif val <= 0xFE:
        # -108 to -1131, represented by 2 bytes
        val2 = int.from_bytes(stream.read(1), byteorder="little")
        decoded = 0x8F - val - (val - 0xFB) * 0xFF - val2
        return decoded

    elif val == 0xFF:
        # 4-byte integer follows
        decoded = int.from_bytes(stream.read(4), byteorder="big", signed=signed)
        return decoded

    raise ValueError


def read_doubles(num, stream):
    # Read a number of doubles from the stream and return them
    return unpack(num * "d", stream.read(num * 8))


def read_floats(num, stream):
    # Read a number of floats from the stream and return them
    return unpack(num * "f", stream.read(num * 4))
