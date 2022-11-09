from struct import unpack
from typing import Any, Dict, List
from vfbLib.parsers import BaseParser, read_encoded_value


class AxisMappingsParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[Dict[str, Any]]:
        mappings = []
        for _ in range(cls.stream.getbuffer().nbytes // 16):
            src = unpack("d", cls.stream.read(8))[0]
            tgt = unpack("d", cls.stream.read(8))[0]
            mappings.append([src, tgt])

        return mappings


class PrimaryInstancesParser(BaseParser):
    @classmethod
    def _parse(cls) -> List[Dict[str, Any]]:
        stream = cls.stream
        instances = []
        num_instances = read_encoded_value(stream)
        for _ in range(num_instances):
            name_length = read_encoded_value(stream)
            name = stream.read(name_length).decode("cp1252")
            values = [read_encoded_value(stream) / 10000 for _ in range(4)]
            instances.append({"name": name, "values": values})

        return instances
