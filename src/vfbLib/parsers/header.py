from __future__ import annotations

import logging
from io import BufferedReader, BytesIO

from vfbLib.parsers.base import StreamReader
from vfbLib.typing import VfbHeaderDict

logger = logging.getLogger(__name__)

# FontLab 3.0 and newer
FL30_SIGNATURE = 0x464C571A  # _WLF

FL30_APP = 0x31
FL30_FILE = 0x30

# FontLab 2.5 (not implemented here)
FL25_SIGNATURE = 0x53564EFF
FL25_APP = 10
FL25_FILE = 13


class VfbHeaderParser(StreamReader):
    def __init__(self, stream: BufferedReader | BytesIO) -> None:
        self.stream = stream

    def parse(self) -> VfbHeaderDict:
        signature = self.read_uint32()
        assert signature == FL30_SIGNATURE, f"File signature not supported: {signature}"
        app_version = self.read_uint8()
        assert app_version == FL30_APP, f"Unsupported app version: {app_version}"
        file_version = self.read_uint8()
        assert file_version == FL30_FILE, f"Unsupported file version: {file_version}"
        version_major = self.read_uint8()
        assert version_major == 3, f"Unsupported app version (major): {version_major}"
        version_minor = self.read_uint8()

        header: VfbHeaderDict = {
            "signature": signature,
            "app_version": app_version,
            "file_version": file_version,
            "version_major": version_major,
            "version_minor": version_minor,
        }

        data_offset = self.read_uint32()
        self.stream.seek(data_offset)

        return header
