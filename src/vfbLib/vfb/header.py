from __future__ import annotations

import logging
from io import BytesIO
from typing import TYPE_CHECKING, Any

from vfbLib.compilers.header import VfbHeaderCompiler
from vfbLib.helpers import hexStr
from vfbLib.parsers.header import VfbHeaderParser

if TYPE_CHECKING:
    from io import BufferedReader


logger = logging.getLogger(__name__)


class VfbHeader:
    def __init__(self) -> None:
        # The original or decompiled data
        self._data: bytes | dict[str, Any] | None = None
        # The parser which can convert data to decompiled
        self.parser = VfbHeaderParser
        # The compiler which can convert the decompiled representation to bytes
        self.compiler = VfbHeaderCompiler

    def as_dict(self) -> dict[str, Any]:
        if isinstance(self.data, bytes):
            return {"decompiled": hexStr(self.data)}
        return {"decompiled": self.data}

    @property
    def data(self) -> bytes | dict[str, Any] | None:
        return self._data

    @data.setter
    def data(self, value: bytes | dict[str, Any] | None) -> None:
        self._data = value

    def compile(self) -> None:
        """
        Compile the header. The result is stored in VfbHeader.data.
        """
        if isinstance(self._data, bytes):
            return

        self._data = self.compiler().compile(self.data)

    def decompile(self) -> None:
        if not isinstance(self.data, bytes):
            # Already decompiled
            return

        byte_data = self.data
        self.data = self.parser(BytesIO(byte_data)).parse()

    def read(self, stream: BufferedReader) -> None:
        # Read and decompile
        self.data = self.parser(stream).parse()
