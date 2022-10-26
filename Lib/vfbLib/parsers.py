from fontTools.misc.textTools import hexStr
from io import BytesIO
from struct import unpack
from typing import Dict, List
from vfbLib.truetype import TT_COMMANDS


uint8 = 1
uint16 = 2
uint32 = 4


cmd_name = {
    0: "move",
    1: "line",
    3: "curve",
    4: "qcurve",
}


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
            stream.read(4), byteorder="little", signed=True
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
        print("EncodedKeyValueParser", cls.__size__)
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


class GlyphParser(BaseParser):
    @classmethod
    def parse_hints(cls, stream: BytesIO, glyphdata: List) -> None:
        hints = dict(x=[], y=[])
        for i in range(2):
            num_hints = read_encoded_value(stream)
            for j in range(num_hints):
                pos = read_encoded_value(stream)
                width = read_encoded_value(stream)
                hints["yx"[i]].append({"pos": pos, "width": width})

        num_replacements = read_encoded_value(stream)
        if num_replacements > 0:
            # print(f"Parsing {num_replacements} records..." )
            replacements = []
            for j in range(num_replacements):
                k = cls.read_uint8(stream)
                val = cls.read_uint8(stream)
                replacements.append(dict(key=k, value=val))
            if replacements:
                hints["replacements"] = replacements

        if hints["x"] or hints["y"]:
            glyphdata.append(dict(hints=hints))

    @classmethod
    def parse_instructions(cls, stream: BytesIO, glyphdata: List) -> None:
        len_commands = read_encoded_value(stream)
        num_commands = read_encoded_value(stream)
        commands = []
        for i in range(num_commands):
            cmd = cls.read_uint8(stream)
            params = [
                read_encoded_value(stream)
                for j in range(len(TT_COMMANDS[cmd]["params"]))
            ]
            commands.append(
                dict(
                    command=TT_COMMANDS[cmd]["name"],
                    params=dict(zip(TT_COMMANDS[cmd]["params"], params)),
                )
            )

        if commands:
            glyphdata.append(dict(commands=commands))

    @classmethod
    def parse_metrics(cls, stream: BytesIO, glyphdata: List) -> None:
        metrics = {
            "width": read_encoded_value(stream),
            "vwidth": read_encoded_value(stream),
        }
        glyphdata.append(dict(metrics=metrics))

    @classmethod
    def parse_anchors(cls, stream: BytesIO, glyphdata: List) -> None:
        anchors = []
        num = read_encoded_value(stream)
        num_anchors = read_encoded_value(stream)
        for i in range(num_anchors):
            x = read_encoded_value(stream)
            y = read_encoded_value(stream)
            anchors.append({"x": x, "y": y})

        if anchors:
            glyphdata.append(dict(anchors=anchors))

    @classmethod
    def parse_outlines(cls, stream: BytesIO, glyphdata: List) -> None:
        # Nodes
        num_nodes = read_encoded_value(stream, debug=False)
        glyphdata.append(dict(num_nodes=num_nodes))
        segments: List[Dict[str, str | int | List[Dict[str, int]]]] = []
        x = 0
        y = 0
        for i in range(num_nodes):
            byte = int.from_bytes(stream.read(1), byteorder="little")
            flags = byte >> 4
            cmd = byte & 0x0F
            segment = dict(type=cmd_name[cmd], flags=flags, points=[])
            points: List[Dict[str, int]] = []

            # End point
            x += read_encoded_value(stream)
            y += read_encoded_value(stream)
            points.append(dict(index=i, x=x, y=y))

            if cmd == 3:  # Curve?
                # Control 1, Control 2
                for j in range(2):
                    x += read_encoded_value(stream)
                    y += read_encoded_value(stream)
                    points.append(dict(x=x, y=y))

            segment["points"] = points
            segments.append(segment)
        glyphdata.append(segments)

    @classmethod
    def parse_values(cls, stream: BytesIO, glyphdata: List) -> None:
        # print("parse_values")
        while True:
            val = stream.read(1)
            if len(val) == 1:
                stream.seek(-1, 1)
            if int.from_bytes(val, byteorder="little") < 0x20:
                return

            val = read_encoded_value(stream)
            glyphdata.append(val)

    @classmethod
    def parse(cls, data: bytes) -> List:
        s = BytesIO(data)
        start = unpack("<5B", s.read(5))
        glyph_name_length = read_encoded_value(s)
        glyph_name = s.read(glyph_name_length)
        # print("**** Glyph:", glyph_name)
        glyphdata = [int.from_bytes(s.read(1), byteorder="little")]  # 0x08
        glyphdata.append(read_encoded_value(s))
        glyphdata.append(read_encoded_value(s))

        cls.parse_outlines(s, glyphdata)

        while True:
            v = int.from_bytes(s.read(1), byteorder="little")
            if v == 0x0F:
                break

            if v == 0x02:
                cls.parse_metrics(s, glyphdata)
            # elif v == 0x01:
            #     values = []
            #     cls.parse_values(s, values)
            #     glyphdata.append({"01": values})
            elif v == 0x03:
                cls.parse_hints(s, glyphdata)
            elif v == 0x04:
                # FIXME: Are those anchors?
                cls.parse_anchors(s, glyphdata)
            elif v == 0x0A:
                cls.parse_instructions(s, glyphdata)
            else:
                pass

        return [
            start,
            glyph_name.decode("cp1252"),
            glyphdata,
            hexStr(s.read()),
        ]


class IntParser(BaseParser):
    """
    A parser that reads data as UInt16.
    """

    @classmethod
    def parse(cls, data):
        return int.from_bytes(data, byteorder="little", signed=False)


class MaskParser(GlyphParser):
    @classmethod
    def parse(cls, data: bytes) -> List:
        s = BytesIO(data)
        glyphdata = []
        glyphdata.append(read_encoded_value(s))
        glyphdata.append(read_encoded_value(s))
        glyphdata.append(read_encoded_value(s))
        glyphdata.append(read_encoded_value(s))
        cls.parse_outlines(s, glyphdata)
        return glyphdata


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
            65: "openTypeOS2SubscriptXSize",
            66: "openTypeOS2SubscriptYSize",
            67: "openTypeOS2SubscriptXOffset",
            68: "openTypeOS2SubscriptYOffset",
            69: "openTypeOS2SuperscriptXSize",
            70: "openTypeOS2SuperscriptYSize",
            71: "openTypeOS2SuperscriptXOffset",
            72: "openTypeOS2SuperscriptYOffset",
            73: "openTypeOS2StrikeoutSize",
            74: "openTypeOS2StrikeoutPosition",
            77: "openTypeOS2TypoAscender",
            78: "openTypeOS2TypoDescender",
            79: "openTypeOS2TypoLineGap",
            81: "openTypeOS2WinAscent",
            82: "openTypeOS2WinDescent",
            92: "averageWidth",
        }
        s = BytesIO(data)
        metrics = []
        cls.read_key_value_pairs_encoded(
            s, num=9, target=metrics, key_names=metrics_names
        )

        k = cls.read_uint8(s)
        # num_values = read_encoded_value(s)
        v = [read_encoded_value(s) for _ in range(5)]
        metrics.append({str(k): v})

        cls.read_key_value_pairs_encoded(
            s, num=15, target=metrics, key_names=metrics_names
        )

        # PANOSE (partial)
        k = cls.read_uint8(s)
        v = [cls.read_uint8(s) for _ in range(10)]
        metrics.append({str(k): v})

        # Vertical Metrics
        cls.read_key_value_pairs_encoded(
            s, num=7, target=metrics, key_names=metrics_names
        )

        # Codepages/Unicode ranges?
        k = cls.read_uint8(s)
        num_values = read_encoded_value(s)
        v = [cls.read_uint8(s) for _ in range(num_values)]
        metrics.append({str(k): v})

        k = cls.read_uint8(s)
        num_values = read_encoded_value(s)
        v = [cls.read_uint8(s) for _ in range(num_values)]
        metrics.append({str(k): v})

        k = cls.read_uint8(s)
        v = [read_encoded_value(s) for _ in range(3)]
        metrics.append({str(k): v})

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


class VfbHeaderParser(BaseParser):
    @classmethod
    def parse(cls, data):
        cls.data = data
        header = []
        header.append({"header0": cls.read_uint8()})
        header.append({"filetype": data.read(5).decode("cp1252")})
        header.append({"header1": cls.read_uint16()})
        header.append({"header2": cls.read_uint16()})
        header.append({"reserved": str(data.read(34))})
        header.append({"header3": cls.read_uint32()})
        header.append({"header4": cls.read_uint32()})
        for i in range(5, 12):
            header.append({f"header{i}": cls.read_uint16()})

        return header
