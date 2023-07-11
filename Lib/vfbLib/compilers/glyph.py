from __future__ import annotations

from struct import pack
from typing import Any
from vfbLib.compilers import BaseCompiler

import logging


logger = logging.getLogger(__name__)


node_types = {
    "move": 0,
    "line": 1,
    "curve": 3,
    "qcurve": 4,
}


class GlyphCompiler(BaseCompiler):
    @classmethod
    def _compile_binary(cls, data):
        # Imported binary data 8-)
        pass

    @classmethod
    def _compile_components(cls, data):
        # Components
        pass

    @classmethod
    def _compile_glyph_name(cls, data):
        # Glyph name
        if "name" in data:
            glyph_name = data["name"].encode("cp1252")
            glyph_name_length = len(glyph_name)
            cls.write_bytes(b"\x01")
            cls.write_encoded_value(glyph_name_length)
            cls.write_bytes(glyph_name)

    @classmethod
    def _compile_guides(cls, data):
        # Guidelines
        pass

    @classmethod
    def _compile_hints(cls, data):
        # PostScript hints
        pass

    @classmethod
    def _compile_instructions(cls, data):
        # TrueType instructions
        pass

    @classmethod
    def _compile_kerning(cls, data):
        # Kerning
        pass

    @classmethod
    def _compile_metrics(cls, data):
        # Metrics
        if "metrics" in data:
            cls.write_bytes(b"\x02")
            for i in range(cls.num_masters):
                x, y = data["metrics"][i]
                cls.write_encoded_value(x)
                cls.write_encoded_value(y)

    @classmethod
    def _compile_outlines(cls, data):
        # Outlines
        cls.write_uint1(8)
        cls.write_encoded_value(cls.num_masters)  # Number of masters
        cls.write_encoded_value(data["outlines_value"])  # ???
        if "nodes" in data:
            cls.write_encoded_value(len(data["nodes"]))  # Number of nodes
            ref_coords = [[0, 0] for _ in range(cls.num_masters)]
            for node in data["nodes"]:
                type_flags = node_types[node["type"]] + node.get("flags", 0) << 4
                cls.write_uint1(type_flags)
                for j in range(len(node["points"][0])):
                    for i in range(cls.num_masters):
                        x, y = node["points"][i][j]
                        # TODO: Make relative to ref_coords
                        cls.write_encoded_value(x)
                        cls.write_encoded_value(y)
        else:
            cls.write_encoded_value(0)

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
        cls.write_bytes(b"\x0f")  # End of glyph
