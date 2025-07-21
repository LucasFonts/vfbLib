from __future__ import annotations

import logging
from collections.abc import Sequence
from math import atan2, degrees
from typing import TYPE_CHECKING, Literal

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import GuideDict, GuidePropertiesDict, GuidePropertyDict
from vfbLib.value import read_value

if TYPE_CHECKING:
    from io import BytesIO

    from vfbLib.typing import MMGuidesDict


logger = logging.getLogger(__name__)


DIRECTIONS: Sequence[Literal["h", "v"]] = ("h", "v")


def parse_guides(stream: BytesIO, num_masters: int, name: str) -> MMGuidesDict:
    # Common parser for glyph and global guides
    guides: MMGuidesDict = {
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
                    guides[d][m].append(GuideDict(pos=pos, angle=angle))
                except ValueError:
                    logger.error(f"Missing {d} guideline data ({name})")
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
        for k in ("h", "v"):
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

                guides[k].append(g)

        return guides
