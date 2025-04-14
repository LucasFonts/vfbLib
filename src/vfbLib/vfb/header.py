from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from vfbLib.compilers.header import VfbHeaderCompiler
from vfbLib.helpers import hexStr
from vfbLib.parsers.header import VfbHeaderParser

if TYPE_CHECKING:
    from io import BufferedReader


logger = logging.getLogger(__name__)


class VfbHeader:
    def __init__(self) -> None:
        # The original or compiled binary data
        self._data: bytes | None = None
        # The decompiled data
        self.decompiled: dict[str, Any] | None = None
        # Has the data been modified, i.e. it needs recompilation
        self.modified = False
        # The parser which can convert data to decompiled
        self.parser = VfbHeaderParser
        # The compiler which can convert the decompiled representation to bytes
        self.compiler = VfbHeaderCompiler

    def as_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"decompiled": self.decompiled}
        if self.data is not None:
            d["data"] = hexStr(self.data)
        return d

    @property
    def data(self) -> bytes | None:
        return self._data

    @data.setter
    def data(self, value: bytes | None) -> None:
        if value != self._data:
            # New compiled data, we should remove the decompiled representation
            self.decompiled = None
        self._data = value

    def compile(self) -> None:
        """
        Compile the header. The result is stored in VfbHeader.data.
        """
        # XXX: Why do we need to always compile?
        # if not self.modified:
        #     return

        self._data = self.compiler().compile(self.decompiled)
        self.modified = False

    def read(self, stream: BufferedReader) -> None:
        self.decompiled = self.parser(stream).parse()
