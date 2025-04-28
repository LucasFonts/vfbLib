from __future__ import annotations

import hashlib
import logging
import pickle
from functools import cached_property
from io import BytesIO
from struct import pack
from typing import TYPE_CHECKING, Any

from vfbLib.compilers.base import BaseCompiler
from vfbLib.constants import parser_classes
from vfbLib.helpers import hexStr
from vfbLib.parsers.base import BaseParser, StreamReader

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
        # The original or compiled binary data
        self.data = None
        # The decompiled data
        self._decompiled: EntryDecompiled = None
        # Temporary data for additional master, must be merged when compiling
        self.temp_masters: list[list] | None = None
        self.parser = None
        self.compiler = None
        # The numeric and human-readable key of the entry, also sets parser & compiler
        self.id = eid
        self.key = None
        # Has the data been modified, i.e. it needs recompilation
        self._modified = False
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
        # The hash of the initial decompiled data is used to detect modifications
        self.store_hash()

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
    def size(self) -> int:
        """The size of the compiled data.

        Returns:
            int: The size of the current compiled data.
        """
        if self.data is None:
            return 0

        return len(self.data)

    @property
    def current_hash(self) -> bytes | None:
        m = hashlib.sha256()
        try:
            m.update(pickle.dumps(self.decompiled))
        except TypeError:
            logger.error("Can not update hash because of unpickleable type:")
            logger.error(self)
            logger.error(type(self.decompiled))
            logger.error(self.decompiled)
            raise
        return m.digest()

    @property
    def data(self) -> bytes | None:
        return self._data

    @data.setter
    def data(self, value: bytes | None) -> None:
        self._data = value

    @property
    def decompiled(self) -> EntryDecompiled:
        return self._decompiled

    @decompiled.setter
    def decompiled(self, value: EntryDecompiled) -> None:
        self._decompiled = value

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

    @property
    def modified(self) -> bool:
        if self.hash is None:
            return True
        return self.current_hash != self.hash

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

    def as_dict(self, minimize=True) -> dict[str, Any]:
        d: dict[str, Any] = {
            "key": str(self.key),
        }
        if minimize:
            if self.decompiled is None:
                d["size"] = self.size
                d["data"] = hexStr(self.data)
            else:
                d["decompiled"] = self.decompiled
        else:
            d["size"] = self.size
            d["data"] = hexStr(self.data)
            if self.parser is not None:
                d["parser"] = self.parser.__name__
            d["decompiled"] = self.decompiled
            if self.compiler is not None:
                d["compiler"] = self.compiler.__name__
            if self.modified:
                d["modified"] = True
        return d

    def clean(self) -> None:
        """
        Reset the entry to its original, un-decompiled state.
        """
        self.decompiled = None
        self.hash = None
        self.store_hash()

    def compile(self, force: bool = False) -> bool:
        """
        Compile the entry. The result is stored in VfbEntry.data.

        Args:
            force (bool, optional): Force compilation even when data has not changed.
                Defaults to False.

        Returns:
            bool: Whether compilation was successful.
        """
        if not (self.modified or force):
            logger.debug(
                "    Skipping entry compilation because it has not been modified: "
                f"'{self.key}'"
            )
            return True

        if self.compiler is None:
            logger.error(
                f"Compiling '{self.id}' is not supported yet in {self} "
                f"Decompiled: {self.decompiled}"
            )
            return False

        self.merge_masters_data()

        self.data = self.compiler().compile(
            self.decompiled, master_count=self.vfb.num_masters
        )

        # TODO: Return False here if compilation has failed. How to tell?

        self.store_hash()
        return True

    def decompile(self) -> None:
        """
        Decompile the entry. The result is stored in VfbEntry.decompiled.
        """
        if self.decompiled is not None:
            # Already decompiled
            if self.modified:
                logger.warning(
                    f"Decompiling a modified entry again: {self.key}."
                    " This will overwrite any modifications in the decompiled data."
                )
                # raise RuntimeError

        if self.parser is None:
            raise ValueError

        if self.data is None:
            raise ValueError

        try:
            self.decompiled = self.parser().parse(
                BytesIO(self.data),
                size=self.size,
                master_count=self.vfb.num_masters,
                ttStemsV_count=self.vfb.ttStemsV_count,
                ttStemsH_count=self.vfb.ttStemsH_count,
            )
        except:  # noqa: E722
            logger.error(f"Parse error for data: {self.key}; {hexStr(self.data)}")
            logger.error(f"Parser class: {self.parser.__name__}")
            self.decompiled = None
            self.error = "ERROR"  # TODO: Include traceback
            self.vfb.any_errors |= True
            # raise
        self.hash = None
        if self.decompiled is not None:
            self.store_hash()

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

        self.compiler.merge(self.temp_masters, self.decompiled)

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

    def store_hash(self) -> None:
        """
        Store a hash of the decompiled data. Can be used to track any changes.
        """
        self.hash = self.current_hash
