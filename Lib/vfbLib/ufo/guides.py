from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vfbLib.ufo.types import (
        GuideList,
        GuideDict,
        GuideAllProperty,
        GuideAllPropertyList,
        GuidePropertyList,
    )


def get_master_guides(
    mm_guides: GuideDict, master_index: int
) -> GuideAllPropertyList:
    # Concatenate guidlines for both directions and extract coords for master_index
    guides = []
    for d in "hv":
        for master_guide in mm_guides[d][master_index]:
            guide: GuideAllProperty = {"x": 0, "y": 0}
            if d == "h":
                guide["y"] = master_guide["pos"]
            else:
                guide["x"] = master_guide["pos"]
            angle = master_guide["angle"]
            if d == "v":
                angle = 90 - angle
            if angle < 0:
                angle += 360
            if angle > 360:
                angle -= 360
            guide["angle"] = round(angle, 2)
            guides.append(guide)
    return guides


def apply_guide_properties(
    guides: GuideAllPropertyList, properties: GuidePropertyList
) -> None:
    # Update the guides with names and colors from properties
    for prop in properties:
        guide_index = prop["index"]
        assert isinstance(guide_index, int)
        guide = guides[guide_index - 1]  # index is 1-based
        if "color" in prop:
            color = prop["color"]
            assert isinstance(color, str)
            r = int(color[1:3], 16) / 0xFF
            try:
                g = int(color[3:5], 16) / 0xFF
            except ValueError:
                g = 0
            try:
                b = int(color[5:7], 16) / 0xFF
            except ValueError:
                b = 0
            guide["color"] = f"{r:0.4f},{g:0.4f},{b:0.4f},1"
        if "name" in prop:
            guide["name"] = prop["name"]
