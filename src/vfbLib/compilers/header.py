from __future__ import annotations

import logging
from io import BytesIO

from vfbLib.compilers.base import StreamWriter
from vfbLib.typing import VfbHeaderDict

logger = logging.getLogger(__name__)


class VfbHeaderCompiler(StreamWriter):
    encoding = "cp1252"

    def compile(self, data: VfbHeaderDict) -> bytes:
        self.stream = BytesIO()
        self._compile(data)
        return self.stream.getvalue()

    def _compile(self, data: VfbHeaderDict) -> None:
        self.write_uint8(data["header0"])
        self.write_str(data["filetype"])
        self.write_uint16(data["header1"])

        # Compile chunk1 separately so we can store its size
        sw = StreamWriter()
        sw.stream = BytesIO()
        for value in data["chunk1"]:
            sw.write_uint8(value)
        chunk1 = sw.stream.getvalue()
        self.write_uint16(len(chunk1))
        self.write_bytes(chunk1)
        if data["chunk1"][-2:] == [10, 0]:
            # FL4+ additions over FL3
            # Compile the app_info chunk separately so we can store its size
            sw = StreamWriter()
            sw.stream = BytesIO()
            for k, v in data["creator"].items():
                sw.write_uint8(k)
                if k == 2:
                    # app version
                    sw.write_uint8(0xFF)
                    for version in v:
                        sw.write_uint8(version)
                else:
                    sw.write_value(v)
            sw.write_uint8(0)  # stop marker of the key-value dict
            app_info = sw.stream.getvalue()
            self.write_uint16(len(app_info))
            self.write_bytes(app_info)
            # In the older header, this is already at the end of chunk1:
            self.write_uint8(6)
            self.write_uint8(1)
        self.write_uint16(0)
