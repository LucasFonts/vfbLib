from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr
from io import BufferedReader
from pathlib import Path
from time import time
from typing import Any, List, Tuple, Type
from vfbLib.constants import ignore_minimal, parser_classes
from vfbLib.parsers import BaseParser
from vfbLib.parsers.header import VfbHeaderParser


logger = logging.getLogger(__name__)

FALLBACK_PARSER = BaseParser


class VFBReader:
    """
    Base class to read data from a vfb file
    """

    def __init__(
        self,
        vfb_path: Path,
        timing=True,
        minimal=False,
        only_keys: List[str] | None = None,
    ) -> None:
        self.vfb_path = vfb_path
        self.data: List[List[Any]] = []
        self.timing = timing
        self.minimal = minimal
        if only_keys is None:
            self.only_keys = []
        else:
            self.only_keys = only_keys
        self.master_count = None

    def __repr__(self) -> str:
        return str(self.data)

    def parse(self, stream: BufferedReader):
        start = time()
        self.stream = stream
        header = VfbHeaderParser.parse(stream)
        self.data.append(["header", header])
        while True:
            try:
                entry = self._parse_entry()
            except EOFError:
                break

            if entry:
                self.data.append(entry)

                # Save information that is needed by parsers

                if entry[0] == "Master Count":
                    if self.master_count is None:
                        self.master_count = entry[1]
                    else:
                        print("WARNING: Redefined master count")

        end = time()
        if self.timing:
            print(
                "Source file was successfully imported in",
                round((end - start) * 1000),
                "ms.",
            )

    def read(self):
        self.data = []
        with open(self.vfb_path, "rb") as vfb:
            self.parse(vfb)

    def _parse_entry(self) -> List[Any]:
        """
        Read, parse and return an entry from the stream
        """
        entry_id, parser_class, size = self._read_entry()

        if (
            self.minimal
            and entry_id in ignore_minimal
            or self.only_keys
            and entry_id not in self.only_keys
        ):
            self.stream.seek(size, 1)
            return []

        try:
            parsed = parser_class.parse(self.stream, size, self.master_count)
        except:  # noqa: E722
            logger.error(
                f"Parse error for data: {entry_id}; {hexStr(self.stream.read(size))}"
            )
            logger.error(f"Parser class: {parser_class}")
            parsed = f"ParseError ({parser_class})"
            raise

        if parsed:
            return [entry_id, parsed]
        else:
            return []

    def _read_entry(self) -> Tuple[str, Type[BaseParser], int]:
        """
        Read an entry from the stream and return its key, specialized parser
        class, and data.
        """
        entry_id = BaseParser.read_uint16(self.stream)
        entry_info = parser_classes.get(
            entry_id & ~0x8000, (str(entry_id), FALLBACK_PARSER)
        )
        key, parser_class = entry_info

        if entry_id == 5:
            # File end marker?
            BaseParser.read_uint16(self.stream)
            two = BaseParser.read_uint16(self.stream)
            if two == 2:
                BaseParser.read_uint16(self.stream)
                raise EOFError

        if entry_id & 0x8000:
            # Uses uint32 for data length
            num_bytes = BaseParser.read_uint32(self.stream)
        else:
            # Uses uint16 for data length
            num_bytes = BaseParser.read_uint16(self.stream)

        return key, parser_class, num_bytes
