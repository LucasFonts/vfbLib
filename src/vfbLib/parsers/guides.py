from __future__ import annotations

import logging
from math import atan2, degrees
from typing import TYPE_CHECKING

from vfbLib import DIRECTIONS
from vfbLib.parsers.base import BaseParser
from vfbLib.typing import GuideDict, GuidePropertiesDict, GuidePropertyDict
from vfbLib.value import read_value

if TYPE_CHECKING:
    from io import BytesIO

    from vfbLib.typing import MMGuidesDict


logger = logging.getLogger(__name__)


def parse_guides(stream: BytesIO, num_masters: int, name: str) -> MMGuidesDict:
    # Common parser for glyph and global guides
    guides: MMGuidesDict = {"h": [], "v": []}
    for direction in DIRECTIONS:
        num_guides = read_value(stream)
        if num_guides == 0:
            continue

        guides[direction] = [[] for _ in range(num_guides)]
        for i in range(num_guides):
            for _ in range(num_masters):
                try:
                    pos = read_value(stream)
                    angle = degrees(atan2(read_value(stream), 10000))
                    guides[direction][i].append(GuideDict(pos=pos, angle=angle))
                except ValueError:
                    logger.error(f"Missing {direction} guideline data ({name})")
                    raise

    return guides


class GlobalGuidesParser(BaseParser):
    def _parse(self) -> MMGuidesDict:
        assert self.master_count is not None
        guides = parse_guides(self.stream, self.master_count, "global")
        assert self.stream.read() == b""
        return guides


class GuidePropertiesParser(BaseParser):
    def _parse(self) -> GuidePropertiesDict:
        guides = GuidePropertiesDict(h=[], v=[])
        for direction in DIRECTIONS:
            while True:
                index = self.read_value()
                if index == 0:
                    break

                g = GuidePropertyDict(index=index)

                color_raw = self.read_value()
                if color_raw > -1:
                    color_bgr = "%06x" % color_raw
                    g["color"] = f"#{color_bgr[4:]}{color_bgr[2:4]}{color_bgr[:2]}"

                name = self.read_str_with_len()
                if name:
                    g["name"] = name

                guides[direction].append(g)

        return guides
