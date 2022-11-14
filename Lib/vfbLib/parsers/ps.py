from vfbLib.parsers import BaseParser
from struct import unpack


class PostScriptInfoParser(BaseParser):
    """
    A parser that reads data as a double-size float.
    """

    @classmethod
    def _parse(cls):
        values = {}
        values["matrix"] = cls.read_double(6)
        values["whatev"] = cls.read_int32()
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
        return values
