from __future__ import annotations

import logging

from struct import unpack
from typing import Any, Dict, List, Tuple
from vfbLib.parsers import BaseParser, read_encoded_value


logger = logging.getLogger(__name__)


class AxisMappingsParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[Tuple[float, float]]:
        assert cls.stream is not None
        mappings = []
        for _ in range(cls.stream.getbuffer().nbytes // 16):
            src_tgt = cls.read_doubles(2)
            mappings.append(src_tgt)

        return mappings


class MasterFlagParser(BaseParser):
    @classmethod
    def _parse(cls) -> Tuple[int, Tuple[Any]]:
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
