from __future__ import annotations

from io import BytesIO

from vfbLib.compilers.base import StreamWriter
from vfbLib.typing import VfbHeaderDict


class VfbHeaderCompiler(StreamWriter):
    def compile(self, data: VfbHeaderDict) -> bytes:
        self.stream = BytesIO()
        self._compile(data)
        return self.stream.getvalue()

    def _compile(self, data: VfbHeaderDict) -> None:
        self.write_uint32(data["signature"])
        self.write_uint8(data["app_version"])
        self.write_uint8(data["file_version"])
        self.write_uint8(data["version_major"])
        self.write_uint8(data["version_minor"])
        # TODO: How is the padding length determined?
        data_offset = 44
        self.write_uint32(data_offset)
        bytes_written = 10
        for _ in range(data_offset - bytes_written):
            self.write_uint8(0)
