from fontTools.misc.textTools import hexStr
from io import BytesIO
from struct import unpack
from typing import Dict, List
from vfbLib.parsers import BaseParser, read_encoded_value
from vfbLib.truetype import TT_COMMANDS


cmd_name = {
    0: "move",
    1: "line",
    3: "curve",
    4: "qcurve",
}


class GlyphParser(BaseParser):
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
    def parse_components(cls, stream: BytesIO, glyphdata: List) -> None:
        components = []
        num = read_encoded_value(stream)
        print(f"{num} components")
        for i in range(num):
            gid = read_encoded_value(stream)
            x = read_encoded_value(stream)
            y = read_encoded_value(stream)
            transform = [cls.read_uint32(stream) for _ in range(4)]
            c = dict(gid=gid, offsetX=x, offsetY=y, transform=transform)
            print(c)
            components.append(c)
        glyphdata.append(dict(components=components))

    @classmethod
    def parse_hints(cls, stream: BytesIO, glyphdata: List) -> None:
        hints = dict(x=[], y=[])
        for i in range(2):
            num_hints = read_encoded_value(stream)
            print(f"{'YX'[i]} hints: {num_hints}")
            for j in range(num_hints):
                pos = read_encoded_value(stream)
                width = read_encoded_value(stream)
                hints["yx"[i]].append({"pos": pos, "width": width})
        num_replacements = read_encoded_value(stream)
        if num_replacements > 0:
            print(f"Parsing {num_replacements} records..." )
            replacements = []
            for j in range(num_replacements):
                k = cls.read_uint8(stream)
                val = read_encoded_value(stream)
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
        # Instructions are ended by 3 * 0!?
        for _ in range(3):
            read_encoded_value(stream)

        # print(f"Commands: {commands}")
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
    def parse_outlines(cls, stream: BytesIO, glyphdata: List) -> None:
        # Nodes
        num_masters = read_encoded_value(stream)
        num_whatever = read_encoded_value(stream)
        num_nodes = read_encoded_value(stream, debug=False)
        print(f"Nodes: {num_nodes}")
        glyphdata.append(dict(num_masters=num_masters))
        segments: List[Dict[str, str | int | List[Dict[str, int]]]] = []
        x = 0
        y = 0
        for i in range(num_nodes):
            byte = cls.read_uint8(stream)
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
        print(segments)
        glyphdata.append(segments)

    # @classmethod
    # def parse_values(cls, stream: BytesIO, glyphdata: List) -> None:
    #     print("parse_values")
    #     raise
    #     while True:
    #         val = stream.read(1)
    #         if len(val) == 1:
    #             stream.seek(-1, 1)
    #         if int.from_bytes(val, byteorder="little") < 0x20:
    #             return

    #         val = read_encoded_value(stream)
    #         glyphdata.append(val)

    @classmethod
    def parse(cls, data: bytes) -> List:
        """
        01090701
        01  92[7]2e 6e 6f 74 64 65 66 # Glyph name
        08  8c bb[48] 93[8]
            00 ab 8b    [  32,    0] move
            01 8b f9a0  [   0,  780] line 32,780
            01 f7fc 8b  [ 360,    0] line 392,780
            01 8b fda0  [   0, -780] line 392, 0
            00 fbcc bb  [-312,   48] move  80, 48
            01 f79c 8b  [ 264,    0] line
            01 8b f940  [   0,  684] line
            01 fb9c 8b  [-264,    0] line
        02  f83c 8b  [ 424,    0]
        03  8b 8b 8b
        04  8b 8b
        0a  a1[22] 8f[4] # TT hinting
            02 8b 8b
            04 8b 8c 89 8a
            04 8b 8f 89 8a
            04 8c 92 89 8a
            8b 8b 8b
        0f
        """
        s = BytesIO(data)
        glyphdata = []
        start = unpack("<4B", s.read(4))
        glyphdata.append(start)
        while True:
            # Read a value to decide what kind of information follows
            v = cls.read_uint8(s)
            print(f"Coming up: {hex(v)}")

            if v == 0x01:
                # Glyph name
                glyph_name_length = read_encoded_value(s)
                glyph_name = s.read(glyph_name_length)
                print(f"Glyph: {glyph_name}")
                glyphdata.append({"name": glyph_name.decode("cp1252")})

            elif v == 0x02:
                # Metrics
                cls.parse_metrics(s, glyphdata)
                # print(glyphdata)
                # print(hexStr(s.read()))
                # raise

            elif v == 0x03:
                # PS Hints
                cls.parse_hints(s, glyphdata)
                # print(glyphdata)
                # print(hexStr(s.read()))
                # raise

            elif v == 0x04:
                # Anchors
                cls.parse_anchors(s, glyphdata)

            elif v == 0x05:
                # Components
                cls.parse_components(s, glyphdata)

            elif v == 0x08:
                # Outlines
                cls.parse_outlines(s, glyphdata)

            elif v == 0x0A:
                # TrueType instructions
                cls.parse_instructions(s, glyphdata)

            elif v == 0x0F:
                print("Glyph done.")
                break

            else:
                print(f"Unhandled info field: {hex(v)}")
                print(hexStr(s.read()))
                raise ValueError

        return glyphdata


class MaskParser(GlyphParser):
    @classmethod
    def parse(cls, data: bytes) -> List:
        s = BytesIO(data)
        glyphdata = []
        glyphdata.append(read_encoded_value(s))  # 8c
        glyphdata.append(cls.read_uint32(s))  # ff05f5e1
        glyphdata.append(cls.read_uint8(s))  # 00
        print(glyphdata)
        cls.parse_outlines(s, glyphdata)
        return glyphdata
