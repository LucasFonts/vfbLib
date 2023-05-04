from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr
from io import BufferedReader
from pathlib import Path
from time import time
from typing import Any, Dict, List, Tuple, Type
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
        header, _header_size = VfbHeaderParser.parse(stream)
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
        class, and data size.
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


class VfbHeader:
    def __init__(self) -> None:
        # The original or compiled binary data
        self.data: bytes | None = None
        # The decompiled data
        self.decompiled = None
        # Has the data been modified, i.e. it needs recompilation
        self.modified = False
        # The parser which can convert data to decompiled
        self.parser = VfbHeaderParser
        # The size of the compiled data
        self.size = 0

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "size": self.size,
            "decompiled": self.decompiled,
            "modified": self.modified,
            "parser": "VfbHeaderParser",
        }
        if self.data:
            d["data"] = hexStr(self.data)
        return d

    def compile(self) -> bytes:
        logger.error("Compiling the VFB header is not supported yet.")

        if self.data:
            self.size = len(self.data)
        else:
            self.size = 0

        self.modified = False

        if self.data is None:
            return b""

        return self.data

    def read(self, stream: BufferedReader) -> None:
        self.decompiled, self.size = self.parser.parse(stream)
        stream.seek(0)
        self.data = stream.read(self.size)


class VfbEntry:
    def __init__(self) -> None:
        # The original or compiled binary data
        self.data: bytes | None = None
        # The decompiled data
        self.decompiled = None
        # The numeric key of the entry
        self.key = None
        # Has the data been modified, i.e. it needs recompilation
        self.modified = False
        # The parser which can convert data to decompiled
        self.parser: Type[BaseParser] | None = None
        # The size of the compiled data
        self.size = 0

    def _read_entry(self) -> Tuple[str, Type[BaseParser], int]:
        """
        Read an entry from the stream and return its key, specialized parser
        class, and data size.
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

    def as_dict(self) -> Dict[str, Any]:
        d = {
            "key": str(self.key),
            "size": self.size,
        }
        if self.data:
            d["data"] = hexStr(self.data)
        if self.decompiled:
            d["decompiled"] = self.decompiled
        if self.modified:
            d["modified"] = self.modified
        if self.parser is not None:
            d["parser"] = str(self.parser.__name__)
        return d

    def compile(self) -> bytes:
        logger.error("Compiling the VFB entries is not supported yet.")

        if self.data:
            self.size = len(self.data)
        else:
            self.size = 0

        self.modified = False

        if self.data is None:
            return b""

        return self.data

    def read(self, stream: BufferedReader) -> None:
        """
        Read the entry from the stream without decompiling the data.
        """
        self.stream = stream
        self.key, self.parser, self.size = self._read_entry()
        self.data = self.stream.read(self.size)


class Vfb:
    """
    Object to represent the vfb data, with the ability to read and write.
    """

    def __init__(
        self,
        vfb_path: Path,
        timing=True,
        minimal=False,
        only_keys: List[str] | None = None,
        only_header=False,
    ) -> None:
        self.vfb_path = vfb_path
        self.timing = timing
        self.minimal = minimal
        if only_keys is None:
            self.only_keys = []
        else:
            self.only_keys = only_keys
        self.only_header = only_header

        self.clear()

    def as_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Return the Vfb structure as Dict, e.g. for saving as JSON.
        """
        d = {}
        if self.header is not None:
            d["header"] = self.header.as_dict()
        if self.entries:
            d["entries"] = [e.as_dict() for e in self.entries]
        return d

    def clear(self):
        """
        Clear any data that may have been read before.
        """
        self.header: VfbHeader | None = None
        self.entries: List[VfbEntry] = []

    def parse(self, stream: BufferedReader):
        """
        Lazily parse the vfb stream, i.e. parse the header, but only read the binary
        data of other entries.
        """
        start = time()
        self.header = VfbHeader()
        self.header.read(stream)
        if self.only_header:
            return

        entry: VfbEntry | None = None
        while True:
            try:
                entry = VfbEntry()
                entry.read(stream)
            except EOFError:
                break

            if entry is not None:
                self.entries.append(entry)

        end = time()
        if self.timing:
            print(
                "Source file was successfully imported in",
                round((end - start) * 1000),
                "ms.",
            )

    def read(self):
        """
        Read data from the file at vfb_path, without decompiling
        """
        self.clear()
        with open(self.vfb_path, "rb") as vfb:
            self.parse(vfb)

    def write(self, out_path: Path) -> None:
        """
        Compile any entries with changes, and write the VFB to out_path.
        """
        if self.header is None:
            raise ValueError

        with open(out_path, "wb") as vfb:
            if self.header.modified:
                self.header.compile()
            assert self.header.data
            vfb.write(self.header.data)

            for entry in self.entries:
                if entry.modified:
                    entry.compile()
                assert entry.data
                vfb.write(entry.data)
