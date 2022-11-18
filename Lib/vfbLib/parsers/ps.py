from __future__ import annotations

from vfbLib.parsers import BaseParser


class PostScriptInfoParser(BaseParser):
    """
    A parser that reads data as a double-size float.
    """

    @classmethod
    def _parse(cls):
        values = {}
        values["font_matrix"] = cls.read_double(6)
        values["force_bold"] = cls.read_int32()
        values["blue_values"] = [cls.read_int32() for _ in range(14)]
        values["other_blues"] = [cls.read_int32() for _ in range(10)]
        values["family_blues"] = [cls.read_int32() for _ in range(14)]
        values["family_other_blues"] = [cls.read_int32() for _ in range(10)]
        values["blue_scale"] = cls.read_double(1)[0]
        values["blue_shift"] = cls.read_uint32()
        values["blue_fuzz"] = cls.read_uint32()
        values["std_hw"] = cls.read_uint32()
        values["std_vw"] = cls.read_uint32()
        values["stem_snap_h"] = [cls.read_uint32() for _ in range(12)]
        values["stem_snap_v"] = [cls.read_uint32() for _ in range(12)]
        values["bounding_box"] = [cls.read_int16() for _ in range(4)]
        values["zzz_whatever"] = [cls.read_int32() for _ in range(3)]  # FIXME
        values["ascender"] = cls.read_int32()
        values["descender"] = cls.read_int32()
        values["x_height"] = cls.read_int32()
        values["cap_height"] = cls.read_int32()
        assert cls.stream.read() == b""
        return values
