from __future__ import annotations

import logging

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import FLVersionDict

logger = logging.getLogger(__name__)


END = 0
PLATFORM = 1
VERSION = 2
OWNER = 3

PLATFORM_WINDOWS = 0
PLATFORM_MACOS = 1

platform_names = {
    PLATFORM_WINDOWS: "windows",
    PLATFORM_MACOS: "macos",
}

platform_ids = {
    "macos": PLATFORM_MACOS,
    "windows": PLATFORM_WINDOWS,
}


class FLVersionParser(BaseParser):
    """
    A parser that reads the FL Version entry.
    """

    def _parse(self) -> FLVersionDict:
        fl_version_info: FLVersionDict = {}
        while True:
            key = self.read_uint8()
            if key == END:
                break
            value = self.read_value()
            if key == PLATFORM:
                fl_version_info["platform"] = platform_names[value]
            elif key == VERSION:
                # Make the version number human-readable
                app_version = []
                for i in (24, 16, 8, 0):
                    # Extract the bytes from the number again
                    app_version.append(value >> i & 0xFF)
                fl_version_info["version"] = tuple(app_version)
            elif key == OWNER:
                fl_version_info["owner"] = value

        return fl_version_info
