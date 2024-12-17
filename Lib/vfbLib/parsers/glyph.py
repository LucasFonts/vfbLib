from __future__ import annotations

import logging
from enum import Enum
from struct import unpack
from typing import TYPE_CHECKING, Any

from fontTools.misc.textTools import hexStr  # , num2binary
from fontTools.ttLib.tables.ttProgram import Program

from vfbLib.parsers.base import BaseParser
from vfbLib.parsers.guides import parse_guides
from vfbLib.truetype import TT_COMMANDS
from vfbLib.typing import (
    Anchor,
    Component,
    GdefDict,
    GlyphData,
    Hint,
    HintDict,
    Instruction,
    LinkDict,
    MaskData,
    MMAnchor,
    MMNode,
    Point,
)
from vfbLib.value import read_value

if TYPE_CHECKING:
    from io import BytesIO


logger = logging.getLogger(__name__)


class PathCommand(Enum):
    move = 0
    line = 1
    curve = 3
    qcurve = 4


def read_absolute_point(
    points: list[list[Any]],
    stream: BytesIO,
    num_masters: int,
    x_masters: list[int],
    y_masters: list[int],
):
    # Read coordinates for all masters from stream, add the points to a list
    # of points per master. Keep track of the relative coordinates reference
    # value in x_masters and y_masters.
    for m in range(num_masters):
        # End point
        xrel = read_value(stream)
        yrel = read_value(stream)
        x_masters[m] += xrel
        y_masters[m] += yrel
        points[m].append((x_masters[m], y_masters[m]))


class GlyphAnchorsParser(BaseParser):
    def _parse(self) -> list[MMAnchor]:
        anchors = []
        num_anchors = self.read_value()
        num_masters = self.read_value()
        for _ in range(num_anchors):
            anchor = MMAnchor(x=[], y=[])
            for _ in range(num_masters):
                anchor["x"].append(self.read_value())
                anchor["y"].append(self.read_value())
            anchors.append(anchor)
        return anchors


class GlyphAnchorsSuppParser(BaseParser):
    def _parse(self) -> list:
        anchors = []
        num_anchors = self.read_value()
        for _ in range(num_anchors):
            hue = self.read_value()
            rv1 = self.read_value()
            anchors.append({"hue": hue, "reserved": rv1})
        return anchors


class GlyphGDEFParser(BaseParser):
    def _parse(self) -> GdefDict:
        gdef: GdefDict = {}
        class_names = {
            0: "unassigned",
            1: "base",
            2: "ligature",
            3: "mark",
            4: "component",
        }
        glyph_class = self.read_value()
        glyph_class_name = class_names.get(glyph_class, "unassigned")
        if glyph_class_name != "unassigned":
            gdef["glyph_class"] = glyph_class_name

        num_anchors = self.read_value()
        anchors = []
        for _ in range(num_anchors):
            anchor_name_length = self.read_value()
            name = None
            if anchor_name_length > 0:
                name = self.read_str(anchor_name_length)

            x = self.read_value()
            x1 = self.read_value()
            y = self.read_value()
            y1 = self.read_value()
            anchor = Anchor(x=x, x1=x1, y=y, y1=y1)
            if name:
                anchor["name"] = name
            anchors.append(anchor)
        if anchors:
            gdef["anchors"] = anchors

        num_carets = self.read_value()
        carets = []
        for _ in range(num_carets):
            pos = self.read_value()
            xxx = self.read_value()
            carets.append((pos, xxx))
        if carets:
            gdef["carets"] = carets

        try:
            num_values = self.read_value()
            values = [self.read_value() for _ in range(num_values)]
            if values:
                gdef["unknown"] = values
        except EOFError:
            pass

        return gdef


class GlyphOriginParser(BaseParser):
    def _parse(self) -> dict[str, Any]:
        x = self.read_int16()
        y = self.read_int16()
        return {"x": x, "y": y}


class GlyphParser(BaseParser):
    def parse_guides(self) -> None:
        # Guidelines
        guides = parse_guides(self.stream, self.master_count, f"glyph '{self.name}'")
        if guides:
            self.glyphdata["guides"] = guides

    def parse_binary(self) -> None:
        # Imported binary TrueType data
        imported: dict[str, Any] = {}
        while True:
            key = self.read_uint8()

            if key == 0x28:
                break

            elif key == 0x29:
                # Metrics
                imported["width"] = self.read_value()
                imported["lsb"] = self.read_value()
                imported["unknown1"] = self.read_value()
                imported["unknown2"] = self.read_value()
                imported["unknown3"] = self.read_value()
                imported["bbox"] = [self.read_value() for _ in range(4)]

            elif key == 0x2A:
                # Outlines
                num_contours = self.read_value()
                imported["endpoints"] = [self.read_value() for _ in range(num_contours)]
                num_nodes = self.read_value()
                nodes = []
                # logger.debug(f"Parsing {num_nodes} nodes...")
                x = 0
                y = 0
                for i in range(num_nodes):
                    x += self.read_value()
                    y += self.read_value()
                    byte = self.read_uint8()
                    flags = byte >> 4
                    cmd = byte & 0x0F
                    node = (hex(cmd), hex(flags), x, y)
                    # logger.debug(f"    {i}: {node}")
                    nodes.append(node)
                if nodes:
                    imported["nodes"] = nodes

            elif key == 0x2B:
                # Instructions
                num_instructions = self.read_value()
                instructions = self.stream.read(num_instructions)
                p = Program()
                p.fromBytecode(instructions)
                imported["instructions"] = p.getAssembly()

            elif key == 0x2C:
                # Probably HDMX data
                num = self.read_value()
                imported["hdmx"] = [self.read_uint8() for _ in range(num)]

            else:
                logger.error(imported)
                logger.error(f"Unknown key in imported binary glyph data: {hex(key)}")
                raise ValueError

        self.glyphdata["imported"] = imported

    def parse_components(self) -> None:
        components = []
        num = self.read_value()
        for i in range(num):
            gid = self.read_value()
            c = Component(gid=gid, offsetX=[], offsetY=[], scaleX=[], scaleY=[])
            for _ in range(self.master_count):
                x = self.read_value()
                y = self.read_value()
                scaleX, scaleY = self.read_doubles(2)
                c["offsetX"].append(x)
                c["offsetY"].append(y)
                c["scaleX"].append(scaleX)
                c["scaleY"].append(scaleY)
            components.append(c)
        self.glyphdata["components"] = components

    def parse_hints(self) -> None:
        hints = HintDict(v=[], h=[])
        for d in ("h", "v"):
            num_hints = self.read_value()
            for _ in range(num_hints):
                master_hints = []
                for _ in range(self.master_count):
                    pos = self.read_value()
                    width = self.read_value()
                    master_hints.append(Hint(pos=pos, width=width))
                hints[d].append(master_hints)

        num_hintmasks = self.read_value()
        if num_hintmasks > 0:
            hintmasks: list[tuple[str, int]] = []
            for _ in range(num_hintmasks):
                k = self.read_uint8()
                val = self.read_value()
                key = {
                    0x01: "h",  # hintmask for hstem
                    0x02: "v",  # hintmask for vstem
                    0xFF: "r",  # Replacement point
                    # FIXME: This seems to be the node index of the replacement
                    # point. But sometimes it is negative, why?
                }[k]
                hintmasks.append((key, val))
            if hintmasks:
                hints["hintmasks"] = hintmasks

        if hints["v"] or hints["h"] or "hintmasks" in hints:
            self.glyphdata["hints"] = hints

    def parse_instructions(self) -> None:
        # Number of bytes for instructions that follow;
        # we don't use it
        _ = self.read_value()
        num_commands = self.read_value()
        commands: list[Instruction] = []
        for i in range(num_commands):
            cmd = self.read_uint8()
            params = [self.read_value() for _ in range(len(TT_COMMANDS[cmd]["params"]))]
            commands.append(
                Instruction(
                    cmd=TT_COMMANDS[cmd]["name"],
                    params=dict(zip(TT_COMMANDS[cmd]["params"], params)),
                )
            )
        # Instructions are ended by 3 * 0!?
        for _ in range(3):
            self.read_value()

        if commands:
            self.glyphdata["tth"] = commands

    def parse_metrics(self) -> None:
        metrics: list[Point] = []
        for _ in range(self.master_count):
            master_metrics = (
                self.read_value(),
                self.read_value(),
            )
            metrics.append(master_metrics)
        self.glyphdata["metrics"] = metrics

    def parse_outlines(self, target: GlyphData | MaskData) -> int:
        # Nodes
        master_count = self.read_value()
        target["num_masters"] = master_count

        # 2 x the number of values to be read after num_nodes, the reason is unclear.
        _ = self.read_value()
        # glyphdata["num_node_values"] = num_node_values

        num_nodes = self.read_value()
        segments: list[MMNode] = []
        x = [0 for _ in range(master_count)]
        y = [0 for _ in range(master_count)]

        for _ in range(num_nodes):
            byte = self.read_uint8()
            flags = byte >> 4
            cmd = PathCommand(byte & 0x0F).name

            # End point
            points: list[list[Point]] = [[] for _ in range(master_count)]
            read_absolute_point(points, self.stream, master_count, x, y)

            if cmd == "curve":
                # First control point
                read_absolute_point(points, self.stream, master_count, x, y)
                # Second control point
                read_absolute_point(points, self.stream, master_count, x, y)

            segment = MMNode(type=cmd, flags=flags, points=points)
            segments.append(segment)
        target["nodes"] = segments
        return master_count

    def parse_kerning(self) -> None:
        num = self.read_value()
        kerning = {}
        for _ in range(num):
            # Glyph index of right kerning partner
            gid = self.read_value()
            values = []
            for _ in range(self.master_count):
                # List of values, one value per master
                values.append(self.read_value())
            kerning[gid] = values
        self.glyphdata["kerning"] = kerning

    def _parse(self) -> dict[str, Any]:
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
        self.glyphdata = GlyphData()
        start = unpack("<4B", self.stream.read(4))
        if start != (1, 9, 7, 1):
            logger.warning(
                f"Unexpected glyph constant: {start}, please notify developer"
            )
        # glyphdata["constants"] = start
        while True:
            # Read a value to decide what kind of information follows
            v = self.read_uint8()

            if v == 0x01:
                # Glyph name
                glyph_name_length = self.read_value()
                glyph_name = self.stream.read(glyph_name_length)
                self.glyphdata["name"] = glyph_name.decode(self.encoding)
                logger.debug(f"Glyph: {self.glyphdata['name']}")
                self.name = self.glyphdata["name"]

            elif v == 0x02:
                # Metrics
                self.parse_metrics()

            elif v == 0x03:
                # PS Hints
                self.parse_hints()

            elif v == 0x04:
                # Guides
                self.parse_guides()

            elif v == 0x05:
                # Components
                self.parse_components()

            elif v == 0x06:
                # Kerning
                self.parse_kerning()

            elif v == 0x08:
                # Outlines
                self.master_count = self.parse_outlines(self.glyphdata)

            elif v == 0x09:
                # Imported binary TrueType data
                self.parse_binary()

            elif v == 0x0A:
                # TrueType instructions
                self.parse_instructions()

            elif v == 0x0F:
                logger.debug("Glyph done.")
                break

            else:
                logger.error(f"Unhandled info field: {hex(v)}")
                logger.error(hexStr(self.stream.read()))
                raise ValueError

        return dict(self.glyphdata)


class GlyphUnicodeParser(BaseParser):
    def _parse(self) -> list:
        unicodes = []
        for _ in range(self.stream.getbuffer().nbytes // 2):
            u = self.read_uint16()
            unicodes.append(u)
        return unicodes


class GlyphUnicodeSuppParser(BaseParser):
    def _parse(self) -> list:
        unicodes = []
        for _ in range(self.stream.getbuffer().nbytes // 4):
            u = self.read_uint32()
            unicodes.append(u)
        return unicodes


class LinkParser(BaseParser):
    def _parse(self) -> dict[str, Any]:
        links = LinkDict(x=[], y=[])
        for i in range(2):
            num = self.read_value()
            for _ in range(num):
                src = self.read_value()
                tgt = self.read_value()
                links["yx"[i]].append([src, tgt])
        return dict(links)


class MaskParser(GlyphParser):
    def _parse(self) -> dict[str, Any]:
        num = self.read_value()
        maskdata = MaskData(num=num)
        for i in range(num):
            maskdata[f"reserved{i}"] = self.read_value()

        # From here, the mask is equal to the outlines
        self.parse_outlines(maskdata)
        return dict(maskdata)


class GlyphSketchParser(BaseParser):
    def _parse(self) -> list[tuple[int, int, int]]:
        num = self.read_value()
        return [
            (self.read_value(), self.read_value(), self.read_value())
            for _ in range(num)
        ]
