from __future__ import annotations

from struct import pack
from typing import Any
from vfbLib.compilers import BaseCompiler
from vfbLib.truetype import TT_COMMAND_CONSTANTS, TT_COMMANDS

import logging


logger = logging.getLogger(__name__)


node_types = {
    "move": 0,
    "line": 1,
    "curve": 3,
    "qcurve": 4,
}


class InstructionsCompiler(BaseCompiler):
    @classmethod
    def _compile(cls, data: Any) -> None:
        cls.write_encoded_value(len(data))
        for cmd in data:
            command_id = TT_COMMAND_CONSTANTS[cmd["cmd"]]
            cls.write_uint1(command_id)
            params = cmd["params"]
            for param_name in TT_COMMANDS[command_id]["params"]:
                cls.write_encoded_value(params[param_name])
        for _ in range(3):
            cls.write_encoded_value(0)


class GlyphCompiler(BaseCompiler):
    @classmethod
    def _compile_binary(cls, data):
        # Imported binary data 8-)
        if not (imported := data.get("imported")):
            return

        logger.warning("Compiling imported binary data is not supported.")
        return

        cls.write_uint1(9)

    @classmethod
    def _compile_components(cls, data):
        # Components
        if not (components := data.get("components")):
            return

        cls.write_uint1(5)
        cls.write_encoded_value(len(components))
        for component in components:
            cls.write_encoded_value(component["gid"])
            for i in range(cls.num_masters):
                cls.write_encoded_value(component["offsetX"][i])
                cls.write_encoded_value(component["offsetY"][i])
                cls.write_float(component["scaleX"][i])
                cls.write_float(component["scaleY"][i])

    @classmethod
    def _compile_glyph_name(cls, data):
        # Glyph name
        if not (name := data.get("name")):
            return

        glyph_name = name.encode("cp1252")
        glyph_name_length = len(glyph_name)
        cls.write_uint1(1)
        cls.write_encoded_value(glyph_name_length)
        cls.write_bytes(glyph_name)

    @classmethod
    def _compile_guides(cls, data):
        # Guidelines
        if not (guides := data.get("guides")):
            return

        logger.warning("Compiling guidelines is not supported.")
        return

        cls.write_uint1(4)

    @classmethod
    def _compile_hints(cls, data):
        # PostScript hints
        if not (hints := data.get("hints")):
            return

        cls.write_uint1(3)
        for direction in ("h", "v"):
            if direction_hints := hints.get(direction):
                cls.write_encoded_value(len(direction_hints))
                for mm_hint in direction_hints:
                    for i in range(cls.num_masters):
                        hint = mm_hint[i]
                        cls.write_encoded_value(hint["pos"])
                        cls.write_encoded_value(hint["width"])
            else:
                cls.write_encoded_value(0)

        if not (hintmasks := hints.get("hintmasks")):
            cls.write_encoded_value(0)
            return

        # FIXME: Implement writing of hintmasks
        # cls.write_encoded_value(len(hintmasks))
        cls.write_encoded_value(0)
        logger.warning("Compilation of hint masks is not supported.")

    @classmethod
    def _compile_instructions(cls, data):
        # TrueType instructions
        if not (tth := data.get("tth")):
            return

        cls.write_uint1(0x0A)
        instructions = InstructionsCompiler.compile(tth)
        cls.write_encoded_value(len(instructions))
        cls.stream.write(instructions)

    @classmethod
    def _compile_kerning(cls, data):
        # Kerning
        if not (kerning := data.get("kerning")):
            return

        cls.write_uint1(6)
        cls.write_encoded_value(len(kerning))
        for gid, values in kerning.items():
            cls.write_encoded_value(gid)
            for value in values:
                cls.write_encoded_value(value)

    @classmethod
    def _compile_metrics(cls, data):
        # Metrics
        if not (metrics := data.get("metrics")):
            return

        cls.write_uint1(2)
        for i in range(cls.num_masters):
            x, y = metrics[i]
            cls.write_encoded_value(x)
            cls.write_encoded_value(y)

    @classmethod
    def _compile_outlines(cls, data):
        # Outlines
        # A minimal outlines structure is always written:
        cls.write_uint1(8)
        cls.write_encoded_value(cls.num_masters)  # Number of masters
        cls.write_encoded_value(data["outlines_value"])  # FIXME: Must be calculated
        if not (nodes := data.get("nodes")):
            cls.write_encoded_value(0)
            return

        cls.write_encoded_value(len(nodes))  # Number of nodes, may be 0
        ref_coords = [[0, 0] for _ in range(cls.num_masters)]
        for node in nodes:
            type_flags = node.get("flags", 0) * 16 + node_types[node["type"]]
            cls.write_uint1(type_flags)
            for j in range(len(node["points"][0])):
                for i in range(cls.num_masters):
                    x, y = node["points"][i][j]
                    refx, refy = ref_coords[i]
                    # Coordinates are written relatively to the previous coords
                    cls.write_encoded_value(x - refx)
                    cls.write_encoded_value(y - refy)
                    ref_coords[i] = [x, y]

    @classmethod
    def _compile(cls, data: Any) -> None:

        # Constants?
        cls.write_bytes(pack("<4B", *data["constants"]))
        cls.num_masters = data["num_masters"]

        cls._compile_glyph_name(data)
        cls._compile_outlines(data)
        cls._compile_metrics(data)
        cls._compile_hints(data)
        cls._compile_guides(data)
        cls._compile_components(data)
        cls._compile_kerning(data)
        cls._compile_binary(data)
        cls._compile_instructions(data)
        cls.write_uint1(15)  # End of glyph
