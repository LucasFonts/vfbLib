from __future__ import annotations

import logging
from io import BytesIO
from struct import pack
from typing import TYPE_CHECKING, Any

from fontTools.ttLib.tables.ttProgram import Program

from vfbLib import DIRECTIONS, GLYPH_CONSTANT, gdef_class_names
from vfbLib.compilers.base import BaseCompiler, StreamWriter
from vfbLib.compilers.guides import GuidesCompiler
from vfbLib.parsers.glyph import PathCommand
from vfbLib.truetype import TT_COMMAND_CONSTANTS, TT_COMMANDS

if TYPE_CHECKING:
    from vfbLib.typing import GdefDict, GlyphData, LinkDict, MaskData, MMAnchorDict


logger = logging.getLogger(__name__)


class GlyphAnchorsCompiler(BaseCompiler):
    def _compile(self, data: list[MMAnchorDict]) -> None:
        self.write_value(len(data), signed=False)
        self.write_value(self.master_count, signed=False)
        for anchor in data:
            for i in range(self.master_count):
                self.write_value(anchor["x"][i])
                self.write_value(anchor["y"][i])


class GlyphAnchorsSuppCompiler(BaseCompiler):
    def _compile(self, data: list[dict[str, int]]) -> None:
        self.write_value(len(data), signed=False)
        for anchor in data:
            self.write_value(anchor["hue"], signed=False)
            self.write_value(anchor["reserved"], signed=False)


class GlyphGDEFCompiler(BaseCompiler):
    def _compile(self, data: GdefDict) -> None:
        c = data.get("glyph_class", "unassigned")
        if c is None:
            gdef_class = 0
        else:
            gdef_class = gdef_class_names.index(c)
        self.write_value(gdef_class, signed=False)

        anchors = data.get("anchors", [])
        self.write_value(len(anchors), signed=False)
        for anchor in anchors:
            self.write_str_with_len(anchor.get("name", ""))
            self.write_value(anchor["x"])
            self.write_value(anchor.get("x1", -1))
            self.write_value(anchor["y"])
            self.write_value(anchor.get("y1", -1))

        carets = data.get("carets", [])
        self.write_value(len(carets), signed=False)
        for pos, xxx in carets:
            self.write_value(pos)
            self.write_value(xxx)

        unknown = data.get("unknown", [])
        self.write_value(len(unknown), signed=False)
        for value in unknown:
            self.write_value(value)


class GlyphCompiler(BaseCompiler):
    @classmethod
    def merge(cls, masters_data: list[Any], data: Any) -> None:
        num_masters = len(masters_data)
        if num_masters < 2:
            return

        for m in range(1, num_masters):
            master_data = masters_data[m]
            # See if there is any data to merge
            if "nodes" in master_data:
                assert "nodes" in data
                for i, tgt in enumerate(data["nodes"]):
                    src = master_data["nodes"][i]
                    for key in ("type", "flags"):
                        assert src[key] == tgt[key]
                    tgt["points"][m] = src["points"][m]

            if "components" in master_data:
                assert "components" in data
                for i, tgt in enumerate(data["components"]):
                    src = master_data["components"][i]
                    for key in ("gid",):
                        assert src[key] == tgt[key]
                    tgt["offsetX"][m] = src["offsetX"][m]
                    tgt["offsetY"][m] = src["offsetY"][m]
                    tgt["scaleX"][m] = src["scaleX"][m]
                    tgt["scaleY"][m] = src["scaleY"][m]

    def _compile_binary(self, data):
        # Imported binary data 8-)
        if not (imported := data.get("imported")):  # noqa: F841
            return

        self.write_uint8(9)

        self.write_uint8(0x29)  # Metrics
        self.write_value(imported["width"], signed=False)
        self.write_value(imported["lsb"])
        self.write_value(imported["unknown1"])
        self.write_value(imported["unknown2"])
        self.write_value(imported["unknown3"])
        for value in imported["bbox"]:
            self.write_value(value)

        # Outlines

        self.write_uint8(0x2A)
        num_contours = imported["num_contours"]  # -1 for composite, so we don't count
        self.write_value(num_contours)
        endpoints = imported.get("endpoints", [])
        if num_contours >= 0 and len(endpoints) != num_contours:
            logger.warning(
                f"Imported binary glyph: Number of contours ({num_contours}) doesn't "
                f"match length of endpoints array ({len(endpoints)})"
            )
        for endpoint in endpoints:
            self.write_value(endpoint, signed=False)
        nodes = imported.get("nodes", [])
        self.write_value(len(nodes), signed=False)  # num_nodes
        x0 = 0
        y0 = 0
        for node in nodes:
            x, y = node["point"]
            self.write_value(x - x0)
            self.write_value(y - y0)
            x0 = x
            y0 = y
            self.write_uint8(node["flags"])

        # TrueType instructions

        instructions = imported.get("instructions")
        self.write_uint8(0x2B)
        if instructions:
            p = Program()
            p.fromAssembly(instructions)
            bytecode = p.getBytecode()
            self.write_value(len(bytecode), signed=False)  # num_bytes
            self.write_bytes(bytecode)
        else:
            self.write_value(0, signed=False)

        # HDMX data

        hdmx = imported.get("hdmx", [])
        self.write_uint8(0x2C)
        self.write_value(len(hdmx), signed=False)
        for value in hdmx:
            self.write_uint8(value)

        self.write_uint8(0x28)  # end

    def _compile_components(self, data):
        # Components
        if not (components := data.get("components")):
            return

        self.write_uint8(5)
        self.write_value(len(components))
        for component in components:
            self.write_value(component["gid"])
            for i in range(self.master_count):
                self.write_value(component["offsetX"][i])
                self.write_value(component["offsetY"][i])
                self.write_double(component["scaleX"][i])
                self.write_double(component["scaleY"][i])

    def _compile_glyph_name(self, data):
        # Glyph name
        if not (name := data.get("name")):
            return

        glyph_name = name.encode("cp1252")
        glyph_name_length = len(glyph_name)
        self.write_uint8(1)
        self.write_value(glyph_name_length)
        self.write_bytes(glyph_name)
        logger.debug(f"Compiling glyph '{name}'")

    def _compile_guides(self, data):
        # Guidelines
        if not (guides := data.get("guides")):
            # TODO: Do we always need to write the guides data?
            # guides = MMGuidesDict(
            #     h=[[] for _ in range(self.master_count)],
            #     v=[[] for _ in range(self.master_count)],
            # )
            return

        self.write_uint8(4)
        gc = GuidesCompiler()
        gc.stream = self.stream
        gc.master_count = self.master_count
        gc._compile(guides)

    def _compile_hints(self, data):
        # PostScript hints
        # To minimize diffs, we always write out hint, but it is not necessary
        hints = data.get("hints", {})
        # We could skip empty hinting:
        if not (hints := data.get("hints")):
            return

        self.write_uint8(3)
        for direction in DIRECTIONS:
            if direction_hints := hints.get(direction):
                self.write_value(len(direction_hints))
                for mm_hint in direction_hints:
                    for i in range(self.master_count):
                        hint = mm_hint[i]
                        self.write_value(hint["pos"])
                        self.write_value(hint["width"])
            else:
                self.write_value(0)

        if not (hintmasks := hints.get("hintmasks")):  # noqa: F841
            self.write_value(0)
            return

        self.write_value(len(hintmasks))
        for k, v in hintmasks:
            key = {
                "h": 0x01,
                "v": 0x02,
                "r": 0xFF,
            }[k]
            self.write_uint8(key)
            self.write_value(v)

    def _compile_instructions(self, data):
        # TrueType instructions
        if not (tth := data.get("tth")):
            # self.write_uint8(0x0A)
            # self.write_value(0)
            return

        self.write_uint8(0x0A)
        instructions = InstructionsCompiler().compile(tth)
        self.write_value(len(instructions))
        self.stream.write(instructions)

    def _compile_kerning(self, data):
        # Kerning
        if not (kerning := data.get("kerning")):
            return

        self.write_uint8(6)
        self.write_value(len(kerning))
        for gid, values in kerning.items():
            self.write_value(gid)
            for value in values:
                self.write_value(value)

    def _compile_metrics(self, data):
        # Metrics
        if not (metrics := data.get("metrics")):
            return

        self.write_uint8(2)
        for i in range(self.master_count):
            x, y = metrics[i]
            self.write_value(x)
            self.write_value(y)

    def compile_outlines(self, data, write_key=True):
        # Outlines
        # A minimal outlines structure is always written:
        if write_key:
            self.write_uint8(8)
        self.write_value(self.master_count)  # Number of masters

        if not (nodes := data.get("nodes")):
            # 0 nodes with 0 values
            self.write_value(0)
            self.write_value(0)
            return

        outlines, num_values = OutlinesCompiler().compile(nodes, self.master_count)
        self.write_value(num_values)
        self.stream.write(outlines)

    def _compile(self, data: Any) -> None:
        # Constants?
        self.write_bytes(pack("<4B", *GLYPH_CONSTANT))
        self.master_count = data["num_masters"]

        self._compile_glyph_name(data)
        self.compile_outlines(data)
        self._compile_metrics(data)
        self._compile_hints(data)
        self._compile_guides(data)
        self._compile_components(data)
        self._compile_kerning(data)
        self._compile_binary(data)
        self._compile_instructions(data)
        self.write_uint8(15)  # End of glyph


class GlyphOriginCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        self.write_int16(data["x"])
        self.write_int16(data["y"])


class GlyphSketchCompiler(BaseCompiler):
    def _compile(self, data: list[tuple[int, int, int]]) -> None:
        self.write_value(len(data), signed=False)
        for a, b, c in data:
            self.write_value(a)
            self.write_value(b)
            self.write_value(c)


class GlyphUnicodesCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        for value in data:
            self.write_uint16(value)


class GlyphUnicodesSuppCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        for value in data:
            self.write_uint32(value)


class InstructionsCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        self.write_value(len(data))
        for cmd in data:
            command_id = TT_COMMAND_CONSTANTS[cmd["cmd"]]
            self.write_uint8(command_id)
            params = cmd["params"]
            for param_name in TT_COMMANDS[command_id]["params"]:
                self.write_value(params[param_name])
        for _ in range(3):
            self.write_value(0)


class OutlinesCompiler(StreamWriter):
    def compile(self, data: Any, num_masters: int) -> tuple[bytes, int]:
        self.master_count = num_masters
        self.stream = BytesIO()
        num_values = self._compile(data)
        return self.stream.getvalue(), num_values

    def _compile(self, data: Any) -> int:
        self.write_value(len(data))  # Number of nodes, may be 0
        num_values = 0
        ref_coords = [[0, 0] for _ in range(self.master_count)]
        for node in data:
            type_flags = node.get("flags", 0) * 16 + PathCommand[node["type"]].value
            self.write_uint8(type_flags)
            num_values += 1
            for j in range(len(node["points"][0])):
                for i in range(self.master_count):
                    x, y = node["points"][i][j]
                    refx, refy = ref_coords[i]
                    # Coordinates are written relatively to the previous coords
                    self.write_value(x - refx)
                    self.write_value(y - refy)
                    num_values += 2
                    ref_coords[i] = [x, y]
        return 2 * num_values


class LinksCompiler(BaseCompiler):
    def _compile(self, data: LinkDict) -> None:
        for direction in ("y", "x"):
            dir_links = data[direction]
            self.write_value(len(dir_links))
            for p0, p1 in dir_links:
                self.write_value(p0)
                self.write_value(p1)


class MaskCompiler(GlyphCompiler):
    def _compile(self, data: MaskData) -> None:
        self.master_count = data["num_masters"]
        self.write_value(data["num"])
        for i in range(data["num"]):
            self.write_value(data[f"reserved{i}"])
        self.compile_outlines(data, write_key=False)


class GlobalMaskCompiler(GlyphCompiler):
    def _compile(self, data: GlyphData) -> None:
        self.master_count = data["num_masters"]
        self.compile_outlines(data, write_key=False)


class MaskMetricsCompiler(BaseCompiler):
    def _compile(self, data: tuple[int, int]) -> None:
        x, y = data
        self.write_int16(x)
        self.write_int16(y)


class MaskMetricsMMCompiler(BaseCompiler):
    def _compile(self, data: list[tuple[int, int]]) -> None:
        for value in data:
            x, y = value
            self.write_value(x)
            self.write_value(y)
