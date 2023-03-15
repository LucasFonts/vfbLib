from __future__ import annotations

from io import BufferedReader, BytesIO
from struct import unpack


def read_encoded_value(stream: BufferedReader | BytesIO, signed=True) -> int:
    val = int.from_bytes(stream.read(1), byteorder="little")
    if val == 0:
        raise EOFError

    # logger.debug(f"Read: {hex(val)}")

    if val < 0x20:
        # logger.debug(f"  Illegal value {hex(val)}. Rest of stream:")
        # logger.debug(hexStr(stream.read()))
        raise ValueError

    elif val < 0xF7:
        decoded = val - 0x8B
        # logger.debug(f"  {hex(val)} - 0x8b = {val - 0x8b}")
        return decoded

    elif val <= 0xFA:
        val2 = int.from_bytes(stream.read(1), byteorder="little")
        # logger.debug(f"  Read next: {hex(val2)}")
        decoded = val - 0x8B + (val - 0xF7) * 0xFF + val2
        # logger.debug(
        #     f"    {hex(val)} - 0x8b + {val - 0xf7} * 0xff + {hex(val2)} = {decoded}"
        # )
        return decoded

    elif val <= 0xFE:
        # Negative
        # FIXME

        val2 = int.from_bytes(stream.read(1), byteorder="little")
        # fb 1f -> 0x8f - 0xfb - 0x1f
        decoded = 0x8F - val - (val - 0xFB) * 0xFF - val2
        # logger.debug(
        #     f"    0x8f - {hex(val)} - {val - 0xf7} * 0xff - {hex(val2)} = {decoded}"
        # )
        return decoded

    elif val == 0xFF:
        # 4-byte integer follows
        decoded = int.from_bytes(stream.read(4), byteorder="big", signed=signed)
        # logger.debug(f"  Read next 4 bytes: {decoded}")
        return decoded

    raise ValueError


def read_doubles(num, stream):
    # Read a number of doubles from the stream and return them
    return unpack(num * "d", stream.read(num * 8))


def read_floats(num, stream):
    # Read a number of floats from the stream and return them
    return unpack(num * "f", stream.read(num * 4))
