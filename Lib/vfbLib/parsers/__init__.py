from fontTools.misc.textTools import hexStr
from io import BytesIO
from struct import unpack
from typing import Dict, List


uint8 = 1
uint16 = 2
uint32 = 4


def read_encoded_value(stream: BytesIO, debug=False) -> int:
    val = int.from_bytes(stream.read(1), byteorder="little")
    if val == 0:
        raise EOFError

    if debug:
        print("Read:", hex(val))

    if val < 0x20:
        if debug:
            print(f"  Illegal value {hex(val)}. Rest of stream:")
            print(hexStr(stream.read()))
        raise ValueError

    elif val < 0xF7:
        decoded = val - 0x8B
        if debug:
            print(f"  {hex(val)} - 0x8b = {val - 0x8b}")
        return decoded

    elif val <= 0xFA:
        val2 = int.from_bytes(stream.read(1), byteorder="little")
        if debug:
            print(f"  Read next: {hex(val2)}")
        decoded = val - 0x8B + (val - 0xF7) * 0xFF + val2
        if debug:
            print(
                f"    {hex(val)} - 0x8b + {val - 0xf7} * 0xff + {hex(val2)} = {decoded}"
            )
        return decoded

    elif val <= 0xFE:
        # Negative
        # FIXME

        val2 = int.from_bytes(stream.read(1), byteorder="little")
        # fb 1f -> 0x8f - 0xfb - 0x1f
        decoded = 0x8F - val - (val - 0xFB) * 0xFF - val2
        if debug:
            print(
                f"    0x8f - {hex(val)} - {val - 0xf7} * 0xff - {hex(val2)} = {decoded}"
            )
        return decoded

    elif val == 0xFF:
        # 4-byte signed integer follows
        decoded = int.from_bytes(
            stream.read(4), byteorder="big", signed=True
        )
        if debug:
            print(f"  Read next 4 bytes: {decoded}")
        return decoded


class BaseParser:
    """
    Base class to read data from a vfb file
    """

    @classmethod
    def parse(cls, data):
        return hexStr(data)

    @classmethod
    def read_uint8(cls, stream=None) -> int:
        if stream is None:
            stream = cls.data
        return int.from_bytes(
            stream.read(uint8), byteorder="little", signed=False
        )

    @classmethod
    def read_uint16(cls, stream=None) -> int:
        if stream is None:
            stream = cls.data
        return int.from_bytes(
            stream.read(uint16), byteorder="little", signed=False
        )

    @classmethod
    def read_uint32(cls, stream=None) -> int:
        if stream is None:
            stream = cls.data
        return int.from_bytes(
            stream.read(uint32), byteorder="little", signed=False
        )


class EncodedKeyValueParser(BaseParser):
    """
    A parser that reads data as key with Yuri's optimized encoded value.
    """

    __size__ = 0

    @classmethod
    def parse(cls, data: bytes) -> List[int]:
        # print("EncodedKeyValueParser", cls.__size__)
        stream = BytesIO(data)
        values = []
        for _ in range(cls.__size__):
            key = cls.read_uint8(stream)
            val = read_encoded_value(stream)
            values.append({key: val})

        # Final?
        values.append({cls.read_uint8(stream): None})
        return values


class EncodedKeyValueParser1742(EncodedKeyValueParser):
    __size__ = 4


class EncodedKeyValueParser1743(EncodedKeyValueParser):
    __size__ = 54


class EncodedValueParser(BaseParser):
    """
    A parser that reads data as Yuri's optimized encoded values.
    """

    @classmethod
    def parse(cls, data) -> List[int]:
        # print("EncodedValueParser.parse", data)
        stream = BytesIO(data)
        values = []
        while True:
            try:
                val = read_encoded_value(stream)
                values.append(val)
            except EOFError:
                # print("EOF")
                return values


class GaspParser(BaseParser):
    """
    A parser that reads data as an array representing Gasp table values.
    """

    @classmethod
    def parse(cls, data):
        gasp = unpack(f"<{len(data) // 2}H", data)
        it = iter(gasp)
        return [
            {
                "maxPpem": a,
                "flags": b,
            }
            for a, b in zip(it, it)
        ]


class GlyphEncodingParser(BaseParser):
    @classmethod
    def parse(cls, data):
        gid = int.from_bytes(data[:2], byteorder="little")
        nam = data[2:].decode("ascii")
        return gid, nam


class IntParser(BaseParser):
    """
    A parser that reads data as UInt16.
    """

    @classmethod
    def parse(cls, data):
        return int.from_bytes(data, byteorder="little", signed=False)


class MetricsParser(BaseParser):
    """
    A parser that reads data as "Metrics and Dimension" values.
    """

    @classmethod
    def read_key_value_pairs_encoded(
        cls,
        stream: BytesIO,
        num: int,
        target: List,
        key_names: Dict[int, str] | None = None,
    ):
        if key_names is None:
            key_names = {}
        for _ in range(num):
            k = cls.read_uint8(stream)
            v = read_encoded_value(stream)
            target.append({key_names.get(k, str(k)): v})

    @classmethod
    def parse(cls, data):
        metrics_names = {
            64: "embedding",
            65: "subscript_x_size",
            66: "subscript_y_size",
            67: "subscript_x_offset",
            68: "subscript_y_offset",
            69: "superscript_x_size",
            70: "superscript_y_size",
            71: "superscript_x_offset",
            72: "superscript_y_offset",
            73: "strikeout_size",
            74: "strikeout_position",
            76: "OpenTypeOS2Panose",
            77: "OpenTypeOS2TypoAscender",
            78: "OpenTypeOS2TypoDescender",
            79: "OpenTypeOS2TypoLineGap",
            81: "OpenTypeOS2WinAscent",
            82: "OpenTypeOS2WinDescent",
            83: "Hdmx PPMs 1",
            88: "Hdmx PPMs 2",
            92: "Average Width",
        }
        s = BytesIO(data)
        metrics = []

        while True:
            k = cls.read_uint8(s)

            if k == 0x32:
                return metrics

            elif k in (0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B):
                metrics.append(
                    {metrics_names.get(k, str(k)): read_encoded_value(s)}
                )

            elif k == 0x3C:
                v = [cls.read_uint8(s) for _ in range(9)]
                metrics.append({metrics_names.get(k, str(k)): v})

            elif k in (0x3D, 0x3E, 0x3F):
                metrics.append(
                    {metrics_names.get(k, str(k)): read_encoded_value(s)}
                )

            elif k in (
                0x40,
                0x41,
                0x42,
                0x43,
                0x44,
                0x45,
                0x46,
                0x47,
                0x48,
                0x49,
                0x4A,
                0x4B,
            ):
                metrics.append(
                    {metrics_names.get(k, str(k)): read_encoded_value(s)}
                )

            elif k == 0x4C:  # PANOSE?
                v = [cls.read_uint8(s) for _ in range(10)]
                metrics.append({metrics_names.get(k, str(k)): v})

            elif k in (0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52):
                metrics.append(
                    {metrics_names.get(k, str(k)): read_encoded_value(s)}
                )

            elif k == 0x5C:
                metrics.append(
                    {metrics_names.get(k, str(k)): read_encoded_value(s)}
                )

            elif k == 0x53:
                num_values = read_encoded_value(s)
                v = [cls.read_uint8(s) for _ in range(num_values)]
                metrics.append({metrics_names.get(k, str(k)): v})

            elif k == 0x54:
                metrics.append(
                    {
                        metrics_names.get(k, str(k)): [
                            read_encoded_value(s),
                            read_encoded_value(s),
                        ]
                    }
                )

            elif k == 0x58:
                num_values = read_encoded_value(s)
                v = [cls.read_uint8(s) for _ in range(num_values)]
                metrics.append({metrics_names.get(k, hex(k)): v})

            else:
                print(f"Unknown key in metrics: {hex(k)}")

        return metrics


class PanoseParser(BaseParser):
    """
    A parser that reads data as an array representing PANOSE values.
    """

    @classmethod
    def parse(cls, data):
        return unpack("<10b", data)


class SignedIntParser(BaseParser):
    """
    A parser that reads data as signed Int16.
    """

    @classmethod
    def parse(cls, data):
        return int.from_bytes(data, byteorder="little", signed=True)


class StringParser(BaseParser):
    """
    A parser that reads data as ASCII-encoded strings.
    """

    @classmethod
    def parse(cls, data):
        return data.decode("cp1252")
