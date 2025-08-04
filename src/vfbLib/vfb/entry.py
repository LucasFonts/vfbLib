from __future__ import annotations

import logging
from functools import cached_property
from io import BytesIO
from struct import pack
from typing import TYPE_CHECKING

from vfbLib.compilers.base import BaseCompiler
from vfbLib.constants import parser_classes
from vfbLib.helpers import hexStr
from vfbLib.parsers.base import BaseParser, StreamReader
from vfbLib.typing import EntryDict

if TYPE_CHECKING:
    from io import BufferedReader

    from vfbLib.typing import EntryDecompiled
    from vfbLib.vfb.vfb import Vfb


logger = logging.getLogger(__name__)


FALLBACK_PARSER = BaseParser


class VfbEntry(StreamReader):
    def __init__(
        self,
        parent: Vfb,
        parser: type[BaseParser] | None = None,
        compiler: type[BaseCompiler] | None = None,
        eid: int | None = None,
    ) -> None:
        # The parent object, Vfb
        self.vfb = parent
        # The original or decompiled data
        self._data: bytes | EntryDecompiled | None = None
        # Temporary data for additional master, must be merged when compiling
        self.temp_masters: list[list] | None = None
        self.parser = None
        self.compiler = None
        # The numeric and human-readable key of the entry, also sets parser & compiler
        self.id = eid
        self.key = None
        # The parser which can convert data to decompiled.
        # Use the arg to override the parser looked up in the id setter only
        if parser is not None:
            logger.warning(f"Overriding parser {self.parser} with {parser}")
            self.parser = parser
        # The compiler which can convert the decompiled to compiled data.
        # Use the arg to override the compiler looked up in the id setter only
        if compiler is not None:
            logger.warning(f"Overriding compiler {self.compiler} with {compiler}")
            self.compiler = compiler

    def __repr__(self) -> str:
        return (
            f"<VfbEntry {self.id} ({self.key}), parser: {self.parser}, "
            f"compiler: {self.compiler}>"
        )

    @cached_property
    def header(self) -> bytes:
        """The entry header.

        Returns:
            bytes: The data of the current entry header.
        """
        if self.id is None:
            logger.error(
                "You need to set VfbEntry.id before accessing its header, "
                "usually by reading the entry from the input stream."
            )
            raise ValueError

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

    @property
    def decompiled(self) -> EntryDecompiled | None:
        """
        Deprecated, use VfbEntry.data
        """
        import warnings

        warnings.warn(
            "VfbEntry.decompiled is deprecated, use VfbEntry.data instead",
            DeprecationWarning,
        )
        if isinstance(self._data, bytes):
            return None

        return self._data

    @property
    def size(self) -> int:
        """The size of the compiled data.

        Returns:
            int: The size of the current compiled data.
        """
        if self.data is None:
            return 0

        if isinstance(self.data, bytes):
            return len(self.data)

        raise RuntimeError

    @property
    def data(self) -> bytes | EntryDecompiled | None:
        return self._data

    @data.setter
    def data(self, value: bytes | EntryDecompiled | None) -> None:
        self._data = value

    @property
    def id(self) -> int | None:
        return self._id

    @id.setter
    def id(self, value: int | None) -> None:
        self._id = value
        self.key = str(self._id)
        self.compiler = None
        if self._id is None:
            self.parser = None
        else:
            entry_info = parser_classes.get(self._id)
            if entry_info is None:
                logger.warning(f"Could not find entry info for ID {self._id}")
                logger.warning(
                    f"Falling back to parser {FALLBACK_PARSER} for ID {self._id}"
                )
                self.parser = FALLBACK_PARSER
            else:
                self.key, self.parser, self.compiler = entry_info
                if self.parser is not None:
                    self.parser.encoding = self.vfb.encoding

    def _read_entry(self) -> int:
        """
        Read an entry from the stream and return its data size.
        """
        raw_id = self.read_uint16()
        self.id = raw_id & ~0x8000

        if self.id == 5:
            # File end marker?
            self.read_uint16()
            two = self.read_uint16()
            if two == 2:
                self.read_uint16()
                raise EOFError

        if raw_id & 0x8000:
            # Uses uint32 for data length
            num_bytes = self.read_uint32()
        else:
            # Uses uint16 for data length
            num_bytes = self.read_uint16()

        return num_bytes

    def as_dict(self, minimize=True) -> EntryDict:
        d = EntryDict(key=str(self.key))
        if isinstance(self.data, bytes):
            d["size"] = self.size
            d["decompiled"] = hexStr(self.data)
        else:
            d["decompiled"] = self.data
        if not minimize:
            if self.parser is not None:
                d["parser"] = self.parser.__name__
            if self.compiler is not None:
                d["compiler"] = self.compiler.__name__
        return d

    def compile(self) -> bool:
        """
        Compile the entry. The result is stored in VfbEntry.data.

        Returns:
            bool: Whether compilation was successful.
        """
        if isinstance(self.data, bytes):
            # Is already compiled
            return True

        if self.compiler is None:
            logger.error(
                f"Compiling '{self.id}' is not supported yet in {self} "
                f"Data: {self.data}"
            )
            return False

        self.merge_masters_data()

        self.data = self.compiler().compile(
            self.data, master_count=self.vfb.num_masters
        )

        # TODO: Return False here if compilation has failed. How to tell?

        return True

    def decompile(self) -> None:
        """
        Decompile the entry. The result is stored in VfbEntry.data.
        """
        if self.parser is None:
            raise ValueError

        if self.data is None:
            raise ValueError

        if not isinstance(self.data, bytes):
            # Already decompiled
            return

        byte_data = self.data

        try:
            self.data = self.parser().parse(
                BytesIO(byte_data),
                size=self.size,
                master_count=self.vfb.num_masters,
                ttStemsV_count=self.vfb.ttStemsV_count,
                ttStemsH_count=self.vfb.ttStemsH_count,
            )
        except:  # noqa: E722
            logger.error(f"Parse error for data: {self.key}; {hexStr(byte_data)}")
            logger.error(f"Parser class: {self.parser.__name__}")
            # self.data = byte_data
            self.error = "ERROR"  # TODO: Include traceback
            self.vfb.any_errors |= True
            raise

    def merge_masters_data(self) -> None:
        """
        Merge any temporary masters data into the main decompiled structure. Such data
        can be added as the result of drawing with a PointPen into a multiple master
        Vfb.
        """
        if self.temp_masters is None:
            return

        if self.vfb.num_masters == 1:
            return

        if self.compiler is None:
            return

        self.compiler.merge(self.temp_masters, self.data)

    def read(self, stream: BufferedReader) -> None:
        """
        Read the entry from the stream without decompiling the data.
        """
        self.stream = stream
        size = self._read_entry()
        if self.key == "1410":
            # FIXME: Special FL3 stuff?
            if size != 4:
                logger.warning(f"Entry 1410 with size {size}")
            self.data = self.stream.read(10)
        else:
            self.data = self.stream.read(size)
