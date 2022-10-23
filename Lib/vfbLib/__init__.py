from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List
from vfbLib.constants import parser_classes
from vfbLib.parsers import VfbHeaderParser, uint8, uint16, uint32


class VFBReader:
    """
    Base class to read data from a vfb file
    """

    def __init__(self, vfb_path: Path) -> None:
        self.vfb_path = vfb_path
        self.data: List[Dict[str, Any]] = []

    def parse(self, vfb: BytesIO):
        header = VfbHeaderParser.parse(vfb)
        self.data.append({"header": header})

    def read(self):
        self.data = []
        with open(self.vfb_path, "rb") as vfb:
            self.parse(vfb)

    def _read_entry(self, stream):
        entry_id = stream.read(uint16)
        parser_class = parser_classes.get(entry_id, entry_id)
        num_bytes = stream.read(uint16)
        if num_bytes > 0:
            data = stream.read(num_bytes)
        else:
            data = b""
        return (entry_id, parser_class, data)
