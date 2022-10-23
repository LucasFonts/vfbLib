from io import BufferedReader
from pathlib import Path
from typing import Any, Dict, List, Tuple
from vfbLib.constants import parser_classes
from vfbLib.parsers import BaseParser, VfbHeaderParser


FALLBACK_PARSER = BaseParser


class VFBReader:
    """
    Base class to read data from a vfb file
    """

    def __init__(self, vfb_path: Path) -> None:
        self.vfb_path = vfb_path
        self.data: List[Dict[str, Any]] = []

    def __repr__(self) -> str:
        return str(self.data)

    def parse(self, stream: BufferedReader):
        self.stream = stream
        header = VfbHeaderParser.parse(stream)
        self.data.append({"header": header})
        self._append_parsed_entry()

        # Glyph records
        glyph_order = []
        entry = self._parse_entry()
        while (
            "Glyph Encoding 0" in entry.keys()
            or "Glyph Encoding 1" in entry.keys()
        ):
            key = list(entry.keys())[0]
            glyph_order.append({"gid": entry[key][0], "name": entry[key][1]})
            entry = self._parse_entry()
        self.data.append({"glyphOrder": glyph_order})
        # Append dangling record after glyph order
        self.data.append(entry)
        while True:
            pos = self.stream.tell()
            try:
                entry = self._parse_entry()
                print(entry)
            except EOFError:
                break
            self.data.append(entry)
            if self.stream.tell() == pos:
                break

    def read(self):
        self.data = []
        with open(self.vfb_path, "rb") as vfb:
            self.parse(vfb)

    def _append_parsed_entry(self):
        """
        Read, parse and append an entry from the stream to the data object
        """
        self.data.append(self._parse_entry())

    def _parse_entry(self):
        """
        Read, parse and return an entry from the stream
        """
        entry_id, parser_class, data = self._read_entry()
        try:
            parsed = parser_class.parse(data)
        except:
            print("Parse error for data:", entry_id, data)
            print("Parser class:", parser_class)
            parsed = f"ParseError ({parser_class})"
        return {entry_id: parsed}

    def _read_entry(self) -> Tuple[str, BaseParser, bytes]:
        """
        Read an entry from the stream and return its key, specialized parser
        class, and data.
        """
        entry_id = BaseParser.read_uint16(self.stream)
        entry_info: Tuple[str, BaseParser] = parser_classes.get(
            entry_id, (str(entry_id), FALLBACK_PARSER)
        )
        key, parser_class = entry_info
        # if parser_class == FALLBACK_PARSER:
        #     print(f"Missing specialised parser for entry id {entry_id}.")
        #     # raise KeyError
        num_bytes = BaseParser.read_uint16(self.stream)
        if num_bytes > 0:
            data = self.stream.read(num_bytes)
        else:
            data = b""
        return key, parser_class, data
