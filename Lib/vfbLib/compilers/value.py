from __future__ import annotations

from fontTools.misc.textTools import deHexStr, hexStr
from io import BufferedWriter, BytesIO
from struct import pack


def write_encoded_value(
    value: int, stream: BufferedWriter | BytesIO, signed=True
) -> None:
    # Encode an integer value and write it to the stream. The "signed" param
    # only applies to the longest representation form.
    if -107 <= value <= 107:
        # 2-byte representation
        encoded = pack(">B", (value + 0x8B))
    elif 107 < value <= 1131:
        # 4-byte representation
        encoded = pack(">H", (value + 0xF694))
    elif -1131 <= value < -107:
        # 4-byte representation, negative values
        encoded = pack(">H", (-value + 0xFA94))
    else:
        # 10-byte representation
        fmt = "i" if signed else "I"
        encoded = pack(f">{fmt}", value)
        stream.write(b"\xFF")
    stream.write(encoded)
