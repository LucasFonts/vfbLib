from __future__ import annotations

import logging

from vfbLib.parsers import BaseParser


logger = logging.getLogger(__name__)


class PostScriptInfoParser(BaseParser):
    """
    A parser that reads data as a double-size float.
    """

    @classmethod
    def _parse(cls):
        values = {}
        values["font_matrix"] = cls.read_doubles(6)
        values["force_bold"] = cls.read_int32()
        values["blue_values"] = [cls.read_int32() for _ in range(14)]
        values["other_blues"] = [cls.read_int32() for _ in range(10)]
        values["family_blues"] = [cls.read_int32() for _ in range(14)]
        values["family_other_blues"] = [cls.read_int32() for _ in range(10)]
        values["blue_scale"] = cls.read_double()
        values["blue_shift"] = cls.read_uint32()
        values["blue_fuzz"] = cls.read_uint32()
        values["std_hw"] = cls.read_uint32()
        values["std_vw"] = cls.read_uint32()
        values["stem_snap_h"] = [cls.read_uint32() for _ in range(12)]
        values["stem_snap_v"] = [cls.read_uint32() for _ in range(12)]
        # The bounding box values only get updated during some actions, e.g.
        # going into PS hinting mode
        values["bounding_box"] = dict(
            zip(
                ["xMin", "yMin", "xMax", "yMax"],
                [cls.read_int16() for _ in range(4)],
            )
        )
        values["adv_width_min"] = cls.read_int32()
        values["adv_width_max"] = cls.read_int32()
        values["adv_width_avg"] = cls.read_int32()
        values["ascender"] = cls.read_int32()
        values["descender"] = cls.read_int32()
        values["x_height"] = cls.read_int32()
        values["cap_height"] = cls.read_int32()
        assert cls.stream.read() == b""
        return values
