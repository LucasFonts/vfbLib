from __future__ import annotations

from math import radians, tan
from typing import TYPE_CHECKING

from vfbLib import DIRECTIONS
from vfbLib.compilers.base import BaseCompiler

if TYPE_CHECKING:
    from vfbLib.typing import GuidePropertiesDict, MMGuidesDict


class GuidesCompiler(BaseCompiler):
    def _compile(self, data: MMGuidesDict) -> None:
        for direction in DIRECTIONS:
            dir_guides = data[direction]
            self.write_value(len(dir_guides))
            for guide in dir_guides:
                for master_index in range(self.master_count):
                    self.write_value(guide[master_index]["pos"])
                    angle = int(tan(radians(guide[master_index]["angle"])) * 10000)
                    self.write_value(angle)


class GuidePropertiesCompiler(BaseCompiler):
    def _compile(self, data: GuidePropertiesDict) -> None:
        for direction in DIRECTIONS:
            dir_guides = data[direction]
            for gpd in dir_guides:
                self.write_value(gpd["index"])
                if color_rgb := gpd.get("color"):
                    # The hash sign must be stripped, and the components reordered BGR
                    color_bgr = f"{color_rgb[5:]}{color_rgb[3:5]}{color_rgb[1:3]}"
                    value = int(color_bgr, 16)
                    self.write_value(value, shortest=False, signed=False)
                else:
                    self.write_value(-1)
                self.write_str_with_len(gpd.get("name"))
            self.write_value(0)
