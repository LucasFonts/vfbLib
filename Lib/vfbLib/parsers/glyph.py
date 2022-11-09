from fontTools.misc.textTools import hexStr
from io import BytesIO
from struct import unpack
from typing import Any, Dict, List
from vfbLib.parsers import BaseParser, read_encoded_value
from vfbLib.truetype import TT_COMMANDS


cmd_name = {
    0: "move",
    1: "line",
    3: "curve",
    4: "qcurve",
}


class GlyphAnchorsParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        stream = cls.stream
        anchors = []
        num_anchors = read_encoded_value(stream)
        num_masters = read_encoded_value(stream)
        for _ in range(num_anchors):
            anchor = {"x": [], "y": []}
            for _ in range(num_masters):
                anchor["x"].append(read_encoded_value(stream))
                anchor["y"].append(read_encoded_value(stream))
            anchors.append(anchor)
        return anchors


class GlyphAnchorsSuppParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        stream = cls.stream
        anchors = []
        num_anchors = read_encoded_value(stream)
        for _ in range(num_anchors):
            a = read_encoded_value(stream)
            b = read_encoded_value(stream)
            anchors.append([a, b])
        return anchors


class GlyphGDEFParser(BaseParser):
    @classmethod
    def _parse(cls) -> Dict[str, Any]:
        stream = cls.stream
        gdef = {}
        class_names = {
            0: "unassigned",
            1: "base",
            2: "ligature",
            3: "mark",
            4: "component",
        }
        glyph_class = read_encoded_value(stream)
        glyph_class_name = class_names.get(glyph_class, glyph_class)
        if glyph_class_name != "unassigned":
            gdef["class"] = glyph_class_name

        num_anchors = read_encoded_value(stream)
        anchors = []
        for _ in range(num_anchors):
            anchor = {}
            anchor_name_length = read_encoded_value(stream)
            if anchor_name_length > 0:
                anchor["name"] = stream.read(anchor_name_length).decode(
                    "cp1252"
                )

            anchor["x"] = read_encoded_value(stream)
            anchor["x1"] = read_encoded_value(stream)
            anchor["y"] = read_encoded_value(stream)
            anchor["y1"] = read_encoded_value(stream)
            anchors.append(anchor)
        if anchors:
            gdef["anchors"] = anchors

        num_carets = read_encoded_value(stream)
        carets = []
        for _ in range(num_carets):
            pos = read_encoded_value(stream)
            xxx = read_encoded_value(stream)
            carets.append([pos, xxx])
        if carets:
            gdef["carets"] = carets

        try:
            num_values = read_encoded_value(stream)
            values = [read_encoded_value(stream) for _ in range(num_values)]
            if values:
                gdef["unknown"] = values
        except EOFError:
            pass

        assert stream.read() == b""
        return gdef


class GlyphOriginParser(BaseParser):
    @classmethod
    def _parse(cls) -> Dict[str, Any]:
        stream = cls.stream
        x = int.from_bytes(stream.read(2), signed=True, byteorder="little")
        y = int.from_bytes(stream.read(2), signed=True, byteorder="little")
        return {"x": x, "y": y}


class GlyphParser(BaseParser):
    @classmethod
    def parse_anchors(
        cls, stream: BytesIO, glyphdata: Dict, num_masters=1
    ) -> None:
        anchors = []
        num = read_encoded_value(stream)
        for i in range(num):
            master_anchors = []
            for m in range(num_masters):
                x = read_encoded_value(stream)
                y = read_encoded_value(stream)
                master_anchors.append({"x": x, "y": y})
            anchors.append(master_anchors)

        # Again?
        num = read_encoded_value(stream)
        for i in range(num):
            master_anchors = []
            for m in range(num_masters):
                x = read_encoded_value(stream)
                y = read_encoded_value(stream)
                master_anchors.append({"x": x, "y": y})
            anchors.append(master_anchors)

        if anchors:
            glyphdata["anchors"] = anchors

    @classmethod
    def parse_components(
        cls, stream: BytesIO, glyphdata: Dict, num_masters=1
    ) -> None:
        components = []
        num = read_encoded_value(stream)
        for i in range(num):
            gid = read_encoded_value(stream)
            c = dict(gid=gid, offsetX=[], offsetY=[], scaleX=[], scaleY=[])
            for _ in range(num_masters):
                x = read_encoded_value(stream)
                y = read_encoded_value(stream)
                scaleX = unpack("d", stream.read(8))
                scaleY = unpack("d", stream.read(8))
                c["offsetX"].append(x)
                c["offsetY"].append(y)
                c["scaleX"].append(scaleX)
                c["scaleY"].append(scaleY)
            components.append(c)
        glyphdata["components"] = components

    @classmethod
    def parse_hints(
        cls, stream: BytesIO, glyphdata: Dict, num_masters=1
    ) -> None:
        hints = dict(x=[], y=[])
        for i in range(2):
            num_hints = read_encoded_value(stream)
            for j in range(num_hints):
                master_hints = []
                for m in range(num_masters):
                    pos = read_encoded_value(stream)
                    width = read_encoded_value(stream)
                    master_hints.append({"pos": pos, "width": width})
                hints["yx"[i]].append(master_hints)

        num_replacements = read_encoded_value(stream)

        if num_replacements > 0:
            replacements = []
            for j in range(num_replacements):
                k = cls.read_uint8(stream)
                val = read_encoded_value(stream)
                replacements.append(dict(key=k, value=val))
            if replacements:
                hints["replacements"] = replacements

        if hints["x"] or hints["y"]:
            glyphdata["hints"] = hints

    @classmethod
    def parse_instructions(cls, stream: BytesIO, glyphdata: Dict) -> None:
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
                    cmd=TT_COMMANDS[cmd]["name"],
                    params=dict(zip(TT_COMMANDS[cmd]["params"], params)),
                )
            )
        # Instructions are ended by 3 * 0!?
        for _ in range(3):
            read_encoded_value(stream)

        if commands:
            glyphdata["tth"] = commands

    @classmethod
    def parse_metrics(
        cls, stream: BytesIO, glyphdata: Dict, num_masters=1
    ) -> None:
        metrics = []
        for _ in range(num_masters):
            master_metrics = {
                "x": read_encoded_value(stream),
                "y": read_encoded_value(stream),
            }
            metrics.append(master_metrics)
        glyphdata["metrics"] = metrics

    @classmethod
    def parse_outlines(cls, stream: BytesIO, glyphdata: Dict) -> int:
        # Nodes
        num_masters = read_encoded_value(stream)
        num_whatever = read_encoded_value(stream)
        num_nodes = read_encoded_value(stream, debug=False)
        glyphdata["num_masters"] = num_masters
        segments: List[Dict[str, str | int | List[Dict[str, int]]]] = []
        x = [0 for _ in range(num_masters)]
        y = [0 for _ in range(num_masters)]
        for i in range(num_nodes):
            byte = cls.read_uint8(stream)
            flags = byte >> 4
            cmd = byte & 0x0F
            segment = dict(type=cmd_name[cmd], flags=flags, points=[])
            for m in range(num_masters):
                master_points: List[Dict[str, int]] = []

                # End point
                x[m] += read_encoded_value(stream)
                y[m] += read_encoded_value(stream)
                master_points.append(dict(x=x[m], y=y[m]))

                if cmd == 3:  # Curve?
                    # Control 1, Control 2
                    for j in range(2):
                        x[m] += read_encoded_value(stream)
                        y[m] += read_encoded_value(stream)
                        master_points.append(dict(x=x[m], y=y[m]))

                segment["points"].append(master_points)
            segments.append(segment)
        glyphdata["nodes"] = segments
        return num_masters

    @classmethod
    def parse_kerning(
        cls, stream: BytesIO, glyphdata: Dict, num_masters=1
    ) -> None:
        num = read_encoded_value(stream)
        kerning = []
        for _ in range(num):
            # Right kerning partner
            gid = read_encoded_value(stream)
            values = []
            for _ in range(num_masters):
                values.append(read_encoded_value(stream))
            kerning.append(dict(gid=gid, values=values))
        glyphdata["kerning"] = kerning

    @classmethod
    def _parse(cls) -> Dict[str, Any]:
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
        s = cls.stream
        glyphdata = {}
        start = unpack("<4B", s.read(4))
        glyphdata["constants"] = start
        num_masters = 1
        while True:
            # Read a value to decide what kind of information follows
            v = cls.read_uint8(s)

            if v == 0x01:
                # Glyph name
                glyph_name_length = read_encoded_value(s)
                glyph_name = s.read(glyph_name_length)
                glyphdata["name"] = glyph_name.decode("cp1252")
                # print("Glyph:", glyphdata["name"])

            elif v == 0x02:
                # Metrics
                cls.parse_metrics(s, glyphdata, num_masters)

            elif v == 0x03:
                # PS Hints
                cls.parse_hints(s, glyphdata, num_masters)

            elif v == 0x04:
                # Anchors
                cls.parse_anchors(s, glyphdata, num_masters)

            elif v == 0x05:
                # Components
                cls.parse_components(s, glyphdata, num_masters)

            elif v == 0x06:
                # Kerning
                cls.parse_kerning(s, glyphdata, num_masters)

            elif v == 0x08:
                # Outlines
                num_masters = cls.parse_outlines(s, glyphdata)

            elif v == 0x0A:
                # TrueType instructions
                cls.parse_instructions(s, glyphdata)

            elif v == 0x0F:
                # print("Glyph done.")
                break

            else:
                print(f"Unhandled info field: {hex(v)}")
                print(hexStr(s.read()))
                raise ValueError

        return glyphdata


class GlyphUnicodeParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        unicodes = []
        for _ in range(cls.stream.getbuffer().nbytes // 2):
            u = cls.read_uint16(cls.stream)
            unicodes.append(u)
        return unicodes


class GlyphUnicodeSuppParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        unicodes = []
        for _ in range(cls.stream.getbuffer().nbytes // 4):
            u = cls.read_uint32(cls.stream)
            unicodes.append(u)
        return unicodes


class LinkParser(BaseParser):
    @classmethod
    def _parse(cls) -> Dict:
        s = cls.stream
        links = dict(x=[], y=[])
        for i in range(2):
            num = read_encoded_value(s)
            for _ in range(num):
                src = read_encoded_value(s)
                tgt = read_encoded_value(s)
                links["yx"[i]].append([src, tgt])
        return links


class MaskParser(GlyphParser):
    @classmethod
    def _parse(cls) -> Dict:
        s = cls.stream
        glyphdata = {}
        num_masters = read_encoded_value(s)
        glyphdata["num_masters"] = num_masters  # 8c
        glyphdata["reserved1"] = cls.read_uint32(s)  # ff05f5e1
        glyphdata["reserved2"] = cls.read_uint8(s)  # 00
        for i in range(num_masters - 1):
            glyphdata[f"m{i}"] = read_encoded_value(s)  # 8b
        # print(glyphdata)
        # From here, the mask is equal to the outlines
        cls.parse_outlines(s, glyphdata)
        return glyphdata
