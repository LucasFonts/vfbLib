from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vfbLib import DIRECTIONS
from vfbLib.ufo.typing import UfoGuide

if TYPE_CHECKING:
    from vfbLib.typing import GuidePropertiesDict, MMGuidesDict


logger = logging.getLogger(__name__)


def get_master_guides(mm_guides: MMGuidesDict, master_index: int) -> list[UfoGuide]:
    # Concatenate guidlines for both directions and extract coords for
    # master_index
    guides = []
    for direction in DIRECTIONS:
        for direction_mm_guide in mm_guides[direction]:
            master_guide = direction_mm_guide[master_index]
            guide = UfoGuide(angle=0, x=0, y=0, _direction=direction)
            if direction == "h":
                guide["y"] = master_guide["pos"]
            else:
                guide["x"] = master_guide["pos"]
            angle = master_guide["angle"]
            if direction == "v":
                angle = 90 - angle
            if angle < 0:
                angle += 360
            if angle > 360:
                angle -= 360
            guide["angle"] = round(angle, 2)
            guides.append(guide)
    return guides


def apply_guide_properties(
    guides: list[UfoGuide], properties: GuidePropertiesDict
) -> None:
    # Update the guides with names and colors from properties

    # Split the guides into h and v again
    direction_guides = {
        "h": [g for g in guides if g["_direction"] == "h"],
        "v": [g for g in guides if g["_direction"] == "v"],
    }

    for direction in DIRECTIONS:
        for prop in properties[direction]:
            guide_index = prop["index"] - 1  # index is 1-based
            if guide_index >= len(direction_guides[direction]):
                logger.info(
                    f"Skipping guide properties, guide is missing ({guide_index})."
                )
                logger.info(prop)
                logger.info(f"{direction}: {direction_guides[direction]}")
                continue

            guide = direction_guides[direction][guide_index]
            if "color" in prop:
                color = prop["color"]
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
    for guide in guides:
        del guide["_direction"]
