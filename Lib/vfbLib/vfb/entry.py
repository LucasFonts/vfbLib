from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr
from functools import cached_property
from io import BytesIO
from struct import pack
from typing import TYPE_CHECKING, Any, Dict, Tuple, Type

# from vfbLib.reader import FALLBACK_PARSER
from vfbLib.compilers import BaseCompiler
from vfbLib.constants import parser_classes
from vfbLib.parsers import BaseParser

if TYPE_CHECKING:
    from io import BufferedReader


logger = logging.getLogger(__name__)


FALLBACK_PARSER = BaseParser


class VfbEntry:
    def __init__(
        self,
        parser: Type[BaseParser] | None = None,
        compiler: Type[BaseCompiler] | None = None,
    ) -> None:
        # The original or compiled binary data
        self.data: bytes | None = None
        # The decompiled data
        self.decompiled = None
        # The numeric and human-readable key of the entry
        self.id = None
        self.key = None
        # Has the data been modified, i.e. it needs recompilation
        self._modified = False
        # The parser which can convert data to decompiled
        self.parser = parser
        # The compiler which can convert the decompiled to compiled data
        self.compiler = compiler

    @cached_property
    def header(self) -> bytes:
        """The entry header.

        Returns:
            bytes: The data of the current entry header.
        """
        header = BytesIO()
        if self.size > 0xFFFF:
            entry_id = self.id | 0x8000
        else:
            entry_id = self.id
        header.write(pack("<H", entry_id))
        if self.size > 0xFFFF:
            header.write(pack("<I", self.size))
        else:
            header.write(pack("<H", self.size))
        return header.getvalue()

    @cached_property
    def size(self) -> int:
        """The size of the compiled data.

        Returns:
            int: The size of the current compiled data.
        """
        return len(self.data)

    @property
    def modified(self) -> bool:
        return self._modified

    @modified.setter
    def modified(self, value) -> None:
        self._modified = value
        if self._modified:
            try:
                delattr(self, "size")
            except AttributeError:
                pass
        else:
            self.size
        # Optimized version?
        # if value:
        #     if self._modified:
        #         # Value has not changed from True
        #         return

        #     # Value has changed from False to True, invalidate caches
        #     try:
        #         delattr(self, "size")
        #     except AttributeError:
        #         pass
        #     return

        # if self._modified:
        #     # Value changes from True to False
        #     self._modified = False
        #     return

        # # Value is False, no change

    def _read_entry(
        self,
    ) -> Tuple[str, Type[BaseParser], Type[BaseCompiler] | None, int]:
        """
        Read an entry from the stream and return its key, specialized parser
        class, and data size.
        """
        self.id = BaseParser.read_uint16(self.stream)
        entry_info = parser_classes.get(
            self.id & ~0x8000, (str(self.id), FALLBACK_PARSER, None)
        )
        key, parser_class, compiler_class = entry_info

        if self.id == 5:
            # File end marker?
            BaseParser.read_uint16(self.stream)
            two = BaseParser.read_uint16(self.stream)
            if two == 2:
                BaseParser.read_uint16(self.stream)
                raise EOFError

        if self.id & 0x8000:
            # Uses uint32 for data length
            num_bytes = BaseParser.read_uint32(self.stream)
        else:
            # Uses uint16 for data length
            num_bytes = BaseParser.read_uint16(self.stream)

        return key, parser_class, compiler_class, num_bytes

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

    def compile(self) -> None:
        """
        Compile the entry. The result is stored in VfbEntry.data.
        """
        if self.compiler is None:
            logger.error(f"Compiling '{self.key}' is not supported yet.")
            return

        self.data = self.compiler.compile(self.decompiled)
        self.modified = False

    def decompile(self) -> None:
        """
        Decompile the entry. The result is stored in VfbEntry.decompiled.
        """
        if self.decompiled is not None:
            # Already decompiled
            return

        if self.parser is None:
            raise ValueError

        if self.data is None:
            raise ValueError

        self.decompiled = self.parser.parse(BytesIO(self.data), size=self.size)

    def read(self, stream: BufferedReader) -> None:
        """
        Read the entry from the stream without decompiling the data.
        """
        self.stream = stream
        self.key, self.parser, self.compiler, size = self._read_entry()
        if self.key == "1410":
            # FIXME: Special FL3 stuff?
            if size != 4:
                print(f"Entry 1410 with size {size}")
            self.data = self.stream.read(10)
        else:
            self.data = self.stream.read(size)
