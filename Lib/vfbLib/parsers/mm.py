from __future__ import annotations

import logging

from struct import unpack
from typing import Any, Dict, List, Tuple
from vfbLib.parsers import BaseParser, read_encoded_value


logger = logging.getLogger(__name__)


class AnisotropicInterpolationsParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[int]:
        # The graph used for anisotropic interpolation maps, for all axes.
        assert cls.stream is not None
        values = []
        while True:
            axis_values = []
            try:
                n = read_encoded_value(cls.stream)
                axis_values = [
                    (read_encoded_value(cls.stream), read_encoded_value(cls.stream))
                    for _ in range(n)
                ]
                values.append(axis_values)
            except EOFError:
                return values


class AxisMappingsCountParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[int]:
        # An array of axis mapping counts per axis, for all 4 axes whether they exist
        # or not.
        # 0300 0000  0000 0000  0000 0000  0000 0000
        # -> [3, 0, 0, 0]
        assert cls.stream is not None
        return [cls.read_uint32() for _ in range(4)]


class AxisMappingsParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[Tuple[float, float]]:
        # 10 pairs of (user, design) coordinates per axis.
        # Look at "Axis Mappings Count" to find out which mappings are used in each axis.
        # The trailing unused fields may contain junk and must be ignored.
        assert cls.stream is not None
        mappings = []
        for _ in range(cls.stream.getbuffer().nbytes // 16):
            src_tgt = cls.read_doubles(2)
            mappings.append(src_tgt)

        return mappings


class MasterLocationParser(BaseParser):
    @classmethod
    def _parse(cls) -> Tuple[int, Tuple[Any]]:
        # The location on all 4 axes for this master
        assert cls.stream is not None
        # FIXME: Might also be 2 uint16:
        master_index = cls.read_uint32()
        flags = cls.read_doubles(4)
        return master_index, flags


class PrimaryInstancesParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[Dict[str, Any]]:
        assert cls.stream is not None
        stream = cls.stream
        instances = []
        num_instances = read_encoded_value(stream)
        for _ in range(num_instances):
            name_length = read_encoded_value(stream)
            name = stream.read(name_length).decode("cp1252")
            values = [read_encoded_value(stream) / 10000 for _ in range(4)]
            instances.append({"name": name, "values": values})

        return instances
