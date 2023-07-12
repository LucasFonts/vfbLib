from __future__ import annotations

import logging

from fontTools.misc.textTools import hexStr
from io import BytesIO
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
        # The numeric key of the entry
        self.key = None
        # Has the data been modified, i.e. it needs recompilation
        self.modified = False
        # The parser which can convert data to decompiled
        self.parser = parser
        # The size of the compiled data
        self.size = 0
        # The compiler which can convert the decompiled to compiled data
        self.compiler = compiler

    def _read_entry(
        self,
    ) -> Tuple[str, Type[BaseParser], Type[BaseCompiler] | None, int]:
        """
        Read an entry from the stream and return its key, specialized parser
        class, and data size.
        """
        entry_id = BaseParser.read_uint16(self.stream)
        entry_info = parser_classes.get(
            entry_id & ~0x8000, (str(entry_id), FALLBACK_PARSER, None)
        )
        key, parser_class, compiler_class = entry_info

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

        if self.data:
            self.size = len(self.data)
        else:
            self.size = 0

        self.modified = False

    def decompile(self):
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
        self.key, self.parser, self.compiler, self.size = self._read_entry()
        self.data = self.stream.read(self.size)
