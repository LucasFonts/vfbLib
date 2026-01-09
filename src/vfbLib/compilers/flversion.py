from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vfbLib.compilers.base import BaseCompiler
from vfbLib.parsers.flversion import END, OWNER, PLATFORM, VERSION, platform_ids

if TYPE_CHECKING:
    from vfbLib.typing import FLVersionDict

logger = logging.getLogger(__name__)


class FLVersionCompiler(BaseCompiler):
    def _compile(self, data: FLVersionDict) -> None:
        self.write_uint8(PLATFORM)
        self.write_value(platform_ids[data["platform"]])

        self.write_uint8(VERSION)
        version_tuple = data["version"]
        assert len(version_tuple) == 4
        self.write_uint8(0xFF)
        for value in version_tuple:
            self.write_uint8(value)

        self.write_uint8(OWNER)
        self.write_value(data["owner"])

        self.write_uint8(END)
