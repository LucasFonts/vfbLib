import logging
from io import BytesIO
from typing import Any

from fontTools.misc.textTools import deHexStr

from vfbLib.compilers.base import StreamWriter

logger = logging.getLogger(__name__)


class VfbHeaderCompiler(StreamWriter):
    encoding = "cp1252"

    def compile(self, data: Any) -> bytes:
        self.stream = BytesIO()
        self._compile(data)
        return self.stream.getvalue()

    def _compile(self, data: Any) -> None:
        self.write_uint8(data["header0"])
        self.write_str(data["filetype"])
        self.write_uint16(data["header1"])
        self.write_uint16(data["header2"])
        self.write_bytes(deHexStr(data["reserved"]))
        self.write_uint16(data["header3"])
        self.write_uint16(data["header4"])
        self.write_uint16(data["header5"])
        self.write_uint16(data["header6"])
        self.write_uint16(data["header7"])
        # > FL3 additions
        self.write_uint16(data["header8"])
        for i in range(9, 12):
            d = data[f"header{i}"]
            assert len(d) == 1
            k, v = tuple(d.items())[0]
            self.write_uint8(int(k))
            self.write_value(v)
        self.write_uint8(data["header12"])
        self.write_uint16(data["header13"])
        self.write_uint16(data["header14"])
