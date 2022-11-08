from io import BytesIO
from typing import Any, Dict, List
from vfbLib.parsers import BaseParser, read_encoded_value


class PrimaryInstancesParser(BaseParser):
    @classmethod
    def parse(cls, data: bytes) -> List[Dict[str, Any]]:
        stream = BytesIO(data)
        instances = []
        num_instances = read_encoded_value(stream)
        for _ in range(num_instances):
            name_length = read_encoded_value(stream)
            name = stream.read(name_length).decode("cp1252")
            values = [read_encoded_value(stream) / 10000 for _ in range(4)]
            instances.append({"name": name, "values": values})

        return instances
