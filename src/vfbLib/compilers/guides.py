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
            # if not dir_guides:
            #     self.write_value(0)
            #     continue

            num_guides = len(dir_guides[0])
            self.write_value(num_guides)
            for guide_index in range(num_guides):
                for master_index in range(self.master_count):
                    guide = dir_guides[master_index][guide_index]
                    self.write_value(guide["pos"])
                    angle = int(tan(radians(guide["angle"])) * 10000)
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
