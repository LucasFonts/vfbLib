from vfbLib import DIRECTIONS
from vfbLib.compilers.base import BaseCompiler
from vfbLib.typing import GuideDict, GuidePropertiesDict


class GuidesCompiler(BaseCompiler):
    def _compile(self, data: GuideDict) -> None:
        pass


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
