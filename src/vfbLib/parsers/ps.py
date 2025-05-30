import logging

from vfbLib.helpers import binaryToIntList
from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class PostScriptInfoParser(BaseParser):
    """
    A parser that reads data into a dict of PostScript font info.
    """

    def _parse(self):
        values = {}
        values["font_matrix"] = self.read_doubles(6)
        values["force_bold"] = self.read_int32()
        values["blue_values"] = [self.read_int32() for _ in range(14)]
        values["other_blues"] = [self.read_int32() for _ in range(10)]
        values["family_blues"] = [self.read_int32() for _ in range(14)]
        values["family_other_blues"] = [self.read_int32() for _ in range(10)]
        values["blue_scale"] = self.read_double()
        values["blue_shift"] = self.read_uint32()
        values["blue_fuzz"] = self.read_uint32()
        values["std_hw"] = self.read_uint32()
        values["std_vw"] = self.read_uint32()
        values["stem_snap_h"] = [self.read_uint32() for _ in range(12)]
        values["stem_snap_v"] = [self.read_uint32() for _ in range(12)]
        # The bounding box values only get updated during some actions, e.g.
        # going into PS hinting mode
        values["bounding_box"] = dict(
            zip(
                ["xMin", "yMin", "xMax", "yMax"],
                [self.read_int16() for _ in range(4)],
            )
        )
        values["adv_width_min"] = self.read_int32()
        values["adv_width_max"] = self.read_int32()
        values["adv_width_avg"] = self.read_int32()
        values["ascender"] = self.read_int32()
        values["descender"] = self.read_int32()
        values["x_height"] = self.read_int32()
        values["cap_height"] = self.read_int32()
        return values


class PostScriptGlobalHintingOptionsParser(BaseParser):
    """
    A parser that reads data as a bitfield describing a glyph's PostScript hinting
    options.
    """

    def _parse(self):
        bits = set(binaryToIntList(self.read_uint16()))
        d = {}
        for k, bit in (
            ("generate_flex", 0),  # Automatically generate Flex hints in T1 and OT
        ):
            if bit in bits:
                bits.discard(bit)
                d[k] = 1

        d["other"] = sorted(bits)
        return d


class PostScriptGlyphHintingOptionsParser(BaseParser):
    """
    A parser that reads data as a bitfield describing a glyph's PostScript hinting
    options.
    """

    def _parse(self):
        bits = set(binaryToIntList(self.read_uint32()))
        d = {}
        for k, bit in (
            ("hint_replacement", 29),  # Hint Replacement
            ("horizontal_3_stem", 30),  # Generate horizontal 3-stem
            ("vertical_3_stem", 31),  # Generate vertical 3-stem
        ):
            if bit in bits:
                bits.discard(bit)
                d[k] = 1

        d["other"] = sorted(bits)
        return d
