from __future__ import annotations

import logging
from io import BytesIO
from typing import TYPE_CHECKING, Any

from vfbLib.compilers.header import VfbHeaderCompiler
from vfbLib.helpers import hexStr
from vfbLib.parsers.header import VfbHeaderParser

if TYPE_CHECKING:
    from io import BufferedReader

    from vfbLib.typing import VfbHeaderDict


logger = logging.getLogger(__name__)


class VfbHeader:
    def __init__(self) -> None:
        # The original or decompiled data
        self._data: bytes | VfbHeaderDict | None = None
        # The parser which can convert data to decompiled
        self.parser = VfbHeaderParser
        # The compiler which can convert the decompiled representation to bytes
        self.compiler = VfbHeaderCompiler

    def as_dict(self) -> dict[str, Any]:
        if isinstance(self.data, bytes):
            return {"decompiled": hexStr(self.data)}
        return {"decompiled": self.data}

    @property
    def data(self) -> bytes | VfbHeaderDict | None:
        return self._data

    @data.setter
    def data(self, value: bytes | VfbHeaderDict | None) -> None:
        self._data = value

    def compile(self) -> None:
        """
        Compile the header. The result is stored in VfbHeader.data.
        """
        if isinstance(self.data, bytes):
            return

        if self.data is None:
            raise TypeError("Can't compile empty header.")

        self.data = self.compiler().compile(self.data)

    def decompile(self) -> None:
        if not isinstance(self.data, bytes):
            # Already decompiled
            return

        byte_data = self.data
        self.data = self.parser(BytesIO(byte_data)).parse()

    def read(self, stream: BufferedReader) -> None:
        # Read and decompile
        self.data = self.parser(stream).parse()
