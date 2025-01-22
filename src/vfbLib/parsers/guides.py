from __future__ import annotations

import logging
from collections.abc import Sequence
from math import atan2, degrees
from typing import TYPE_CHECKING, Literal

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import Guide, GuideProperty
from vfbLib.value import read_value

if TYPE_CHECKING:
    from io import BytesIO

    from vfbLib.typing import GuideDict


logger = logging.getLogger(__name__)


DIRECTIONS: Sequence[Literal["h", "v"]] = ("h", "v")


def parse_guides(stream: BytesIO, num_masters: int, name: str) -> GuideDict:
    # Common parser for glyph and global guides
    guides: GuideDict = {
        "h": [[] for _ in range(num_masters)],
        "v": [[] for _ in range(num_masters)],
    }
    for d in DIRECTIONS:
        num_guides = read_value(stream)
        for _ in range(num_guides):
            for m in range(num_masters):
                try:
                    pos = read_value(stream)
                    angle = degrees(atan2(read_value(stream), 10000))
                    guides[d][m].append(Guide(pos=pos, angle=angle))
                except ValueError:
                    logger.error(f"Missing {d} guideline data ({name})")
                    raise

    return guides


class GlobalGuidesParser(BaseParser):
    def _parse(self) -> GuideDict:
        assert self.master_count is not None
        guides = parse_guides(self.stream, self.master_count, "global")
        assert self.stream.read() == b""
        return guides


class GuidePropertiesParser(BaseParser):
    def _parse(self) -> list:
        guides = []
        for _ in range(2):
            while True:
                index = self.read_value()
                if index == 0:
                    break

                g = GuideProperty(index=index)

                color = self.read_value()
                if color > -1:
                    g["color"] = "#" + hex(color & ~0xFF00000000)[2:]

                name_length = self.read_value()
                if name_length > 0:
                    name = self.stream.read(name_length).decode("cp1252")
                    g["name"] = name

                guides.append(g)

        return guides
